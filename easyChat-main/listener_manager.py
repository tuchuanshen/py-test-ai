import threading
import time
from typing import Dict, Callable, List, Optional
from ui_auto_wechat import WeChat


class ListenerManager:
    """
    监听管理器，用于管理多个对象的监听功能
    支持为不同对象设置不同的消息处理函数
    """
    
    def __init__(self, wechat: WeChat):
        """
        初始化监听管理器
        :param wechat: WeChat实例
        """
        self.wechat = wechat
        # 存储监听对象及其对应的消息处理函数
        self.listeners: Dict[str, Callable] = {}
        # 存储监听状态
        self.listening = False
        # 全局监听线程
        self.global_thread: Optional[threading.Thread] = None
        # 单独监听线程字典
        self.individual_threads: Dict[str, threading.Thread] = {}
        # 线程停止事件
        self.stop_events: Dict[str, threading.Event] = {}
        # 线程安全锁
        self.listeners_lock = threading.RLock()
        # 动态添加监听对象时的通知事件
        self.new_listener_event: Optional[threading.Event] = None
        
    def add_listener(self, contact_name: str, message_handler: Optional[Callable] = None) -> None:
        """
        增加监听对象
        :param contact_name: 联系人名称
        :param message_handler: 消息处理函数，如果为None则使用默认处理函数
        """
        with self.listeners_lock:
            if message_handler is None:
                # 默认消息处理函数
                message_handler = self._default_message_handler
                
            self.listeners[contact_name] = message_handler
            print(f"已添加监听对象: {contact_name}")
            
            # 如果正在全局监听，通知监听线程有新对象添加
            if self.listening and self.new_listener_event:
                self.new_listener_event.set()
                self.new_listener_event.clear()
        
    def remove_listener(self, contact_name: str) -> bool:
        """
        删除监听对象
        :param contact_name: 联系人名称
        :return: 是否成功删除
        """
        with self.listeners_lock:
            if contact_name in self.listeners:
                # 停止该对象的单独监听线程（如果存在）
                if contact_name in self.stop_events:
                    self.stop_events[contact_name].set()
                    del self.stop_events[contact_name]
                    
                if contact_name in self.individual_threads:
                    del self.individual_threads[contact_name]
                    
                del self.listeners[contact_name]
                print(f"已删除监听对象: {contact_name}")
                return True
            else:
                print(f"监听对象 {contact_name} 不存在")
                return False
                
    def _default_message_handler(self, contact_name: str, messages: List) -> None:
        """
        默认消息处理函数
        :param contact_name: 联系人名称
        :param messages: 消息列表
        """
        print(f"收到来自 {contact_name} 的消息:")
        for msg_type, sender, content in messages:
            print(f"  [{msg_type}] {sender}: {content}")
            
    def _global_listener_worker(self, check_interval: int = 5) -> None:
        """
        全局监听工作线程
        :param check_interval: 检查间隔（秒）
        """
        print("全局监听线程已启动")
        # 创建通知事件
        self.new_listener_event = threading.Event()
        
        while self.listening:
            try:
                # 检查新消息
                self.wechat.check_new_msg()
                
                # 为每个监听对象获取并处理消息
                with self.listeners_lock:
                    listeners_copy = dict(self.listeners)
                    
                for contact_name, handler in listeners_copy.items():
                    try:
                        # 获取最近的消息（这里简单获取最近5条）
                        messages = self.wechat.get_dialogs(contact_name, 5)
                        if messages:
                            handler(contact_name, messages)
                    except Exception as e:
                        print(f"处理 {contact_name} 的消息时出错: {e}")
                        
                # 等待下次检查或新监听对象添加事件
                self.new_listener_event.wait(check_interval)
                
            except KeyboardInterrupt:
                print("监听线程被用户中断")
                break
            except Exception as e:
                print(f"监听过程中发生错误: {e}")
                self.new_listener_event.wait(check_interval)
                
        print("全局监听线程已停止")
        self.new_listener_event = None
        
    def start_global_listening(self, check_interval: int = 5) -> None:
        """
        启动全局监听线程，一个线程处理所有监听对象
        :param check_interval: 检查间隔（秒）
        """
        if self.listening:
            print("监听已在运行中")
            return
            
        self.listening = True
        self.global_thread = threading.Thread(
            target=self._global_listener_worker,
            args=(check_interval,),
            daemon=True
        )
        self.global_thread.start()
        print("已启动全局监听")
        
    def stop_global_listening(self) -> None:
        """
        停止全局监听
        """
        self.listening = False
        if self.global_thread and self.global_thread.is_alive():
            # 通知线程退出
            if self.new_listener_event:
                self.new_listener_event.set()
            self.global_thread.join(timeout=2)
        print("已停止全局监听")
        
    def _individual_listener_worker(self, contact_name: str, check_interval: int = 5) -> None:
        """
        单独监听工作线程
        :param contact_name: 联系人名称
        :param check_interval: 检查间隔（秒）
        """
        print(f"启动 {contact_name} 的单独监听线程")
        stop_event = self.stop_events[contact_name]
        
        while not stop_event.is_set():
            try:
                # 检查新消息
                self.wechat.check_new_msg()
                
                # 获取并处理特定联系人的消息
                with self.listeners_lock:
                    listener_exists = contact_name in self.listeners
                    if listener_exists:
                        handler = self.listeners[contact_name]
                
                if listener_exists:
                    try:
                        # 获取最近的消息（这里简单获取最近5条）
                        messages = self.wechat.get_dialogs(contact_name, 5)
                        if messages:
                            handler(contact_name, messages)
                    except Exception as e:
                        print(f"处理 {contact_name} 的消息时出错: {e}")
                        
                # 等待下次检查或停止信号
                stop_event.wait(check_interval)
                
            except Exception as e:
                print(f"监听 {contact_name} 时发生错误: {e}")
                stop_event.wait(check_interval)
                
        print(f"{contact_name} 的监听线程已停止")
        
    def start_individual_listening(self, contact_name: Optional[str] = None, check_interval: int = 5) -> None:
        """
        为监听对象启动单独的监听线程
        :param contact_name: 特定联系人名称，如果为None则为所有监听对象启动单独线程
        :param check_interval: 检查间隔（秒）
        """
        # 如果提供了特定联系人
        if contact_name:
            # 检查联系人是否存在
            with self.listeners_lock:
                if contact_name not in self.listeners:
                    print(f"监听对象 {contact_name} 不存在")
                    return
                    
            # 检查是否已经为该联系人启动了监听线程
            if contact_name in self.individual_threads:
                thread = self.individual_threads[contact_name]
                if thread.is_alive():
                    print(f"已为 {contact_name} 启动监听线程")
                    return
                    
            # 创建停止事件
            self.stop_events[contact_name] = threading.Event()
            
            # 启动线程
            thread = threading.Thread(
                target=self._individual_listener_worker,
                args=(contact_name, check_interval),
                daemon=True
            )
            self.individual_threads[contact_name] = thread
            thread.start()
            print(f"已为 {contact_name} 启动单独监听线程")
        else:
            # 为所有监听对象启动单独线程
            with self.listeners_lock:
                listeners_copy = list(self.listeners.keys())
                
            for name in listeners_copy:
                self.start_individual_listening(name, check_interval)
                
    def stop_individual_listening(self, contact_name: Optional[str] = None) -> None:
        """
        停止监听对象的单独监听线程
        :param contact_name: 特定联系人名称，如果为None则停止所有单独监听线程
        """
        if contact_name:
            # 停止特定联系人的监听线程
            if contact_name in self.stop_events:
                self.stop_events[contact_name].set()
                del self.stop_events[contact_name]
                
            if contact_name in self.individual_threads:
                thread = self.individual_threads[contact_name]
                if thread.is_alive():
                    thread.join(timeout=2)
                del self.individual_threads[contact_name]
                
            print(f"已停止 {contact_name} 的单独监听线程")
        else:
            # 停止所有单独监听线程
            with self.listeners_lock:
                stop_names = list(self.stop_events.keys())
                
            for name in stop_names:
                self.stop_individual_listening(name)
                
    def get_listeners(self) -> List[str]:
        """
        获取所有监听对象列表
        :return: 监听对象列表
        """
        with self.listeners_lock:
            return list(self.listeners.keys())
        
    def set_message_handler(self, contact_name: str, message_handler: Callable) -> bool:
        """
        为监听对象设置消息处理函数
        :param contact_name: 联系人名称
        :param message_handler: 消息处理函数
        :return: 是否设置成功
        """
        with self.listeners_lock:
            if contact_name in self.listeners:
                self.listeners[contact_name] = message_handler
                print(f"已为 {contact_name} 设置消息处理函数")
                return True
            else:
                print(f"监听对象 {contact_name} 不存在")
                return False