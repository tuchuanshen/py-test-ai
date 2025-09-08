from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select as SE
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains as AC
from time import sleep
import time

import os, logging, re


class ColouredFormatter(logging.Formatter):
    _lookup = {
        logging.INFO: "\033[1;54m%s\033[1;0m",
        logging.WARNING: "\033[1;93m%s\033[1;0m",
        logging.ERROR: "\033[1;91m%s\033[1;0m",
    }

    def format(self, record):
        result = super().format(record)
        formatted_levelname = self._lookup[record.levelno] % record.levelname
        if '步骤' in result:
            msg = re.findall('(?<=]).*$', result)[0]
            result = re.sub(rf'(?<=]).*$',
                            f'\033[0;34m{msg}\033[0m',
                            result,
                            count=1)
        elif 'print exec cmd on server' in result:
            msg = re.findall('(?<=]).*$', result)[0]
            result = re.sub(rf'(?<=]).*$',
                            f'\033[0;32m{msg}\033[0m',
                            result,
                            count=1)
        result = re.sub(rf'\[({record.levelname})\]',
                        formatted_levelname,
                        result,
                        count=1)
        return result


class Logger():

    def __init__(self, level='info'):
        self.level_ralations = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL,
        }
        self._level = level
        self._logname = ""
        self.logger = logging.getLogger("log")
        self.logger.setLevel(self.level_ralations.get(self._level))
        # self.formater = FilterFormatter('%(asctime)s | %(levelname)s | %(message)s')
        self.formater = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s')
        self.lines = 0
        self.max_lines = -1

        # 控制台输出格式
        self.console = logging.StreamHandler()
        self.console.setLevel(self.level_ralations.get(self._level))
        # self.console.setFormatter(self.formater)
        self.console.setFormatter(
            ColouredFormatter(fmt="%(asctime)s [%(levelname)s] %(message)s"))

    def __strip_too_long_line(self, msg):
        msg_len = len(msg)
        if msg_len > 3000:
            strip_char = msg_len - 2999
            return msg[
                0:
                2999] + f"    ............  LINE TOO LONG, skip {strip_char} chars!"
        else:
            return msg

    def debug(self, msg):
        for line in msg.split('\n'):
            self.logger.debug(self.__strip_too_long_line(line))

    def info(self, msg):
        for line in msg.split('\n'):
            if self.max_lines > 1:
                self.lines += 1
                if self.lines == self.max_lines:
                    self.logger.warning(
                        f"当前用例日志行数为{self.lines},大于系统规定的用例最大日志行数{self.max_lines},后续日志不记录!"
                    )
                    return
                elif self.lines > self.max_lines:
                    return
            self.logger.info(self.__strip_too_long_line(line))

    def warn(self, msg):
        for line in msg.split('\n'):
            self.logger.warning(self.__strip_too_long_line(line))

    def error(self, msg):
        for line in msg.split('\n'):
            self.logger.error(self.__strip_too_long_line(line))

    def fatal(self, msg):
        for line in msg.split('\n'):
            self.logger.fatal(self.__strip_too_long_line(line))

    def log(self, level, msg):
        for line in msg.split('\n'):
            self.logger.log(level, line)

    def save_log(self, logname):
        self._logname = logname
        self.filelogger = logging.FileHandler(self._logname,
                                              mode='a',
                                              encoding="UTF-8")
        self.filelogger.setLevel(self.level_ralations.get(self._level))
        self.filelogger.setFormatter(self.formater)
        self.logger.addHandler(self.filelogger)
        self.logger.addHandler(self.console)

    def set_level(self, level):
        self.console.setLevel(level)
        if self._logname != "":
            self.filelogger.setLevel(level)

    def set_log_maxlines(self, maxlines):
        self.lines = 0
        self.max_lines = maxlines


logger = Logger()

# 获取工程的根路径
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

###########################################################
# 基于selenium接口二次封装底层操作类，采用页面描述和元素描述。命名原则尽量不改变原方法名或者见名知其意。
# 操作主要分为常用的浏览器操作，元素操作，鼠标操作，键盘操作，和js操作，需要相应操作可以到对应模块寻找。
#
###########################################################


class BasePage:
    """基于原生selenium第二次封装"""

    def __init__(self, driver, pagename=''):
        """
        :param driver: 浏览器对象
        :param pagename: 页面名，用于记录log和失败截图
        """
        self.driver = driver
        self.page = pagename

    # #############浏览器操作部分#############
    def get(self, url):
        """
        发送url请求
        :param url: 请求url
        :return: None
        """
        try:
            logger.info(f'打开:{url}')
            self.driver.get(url)
        except Exception:
            raise

    def find_element(self, loc, msg=''):
        """自动显示等待10s,定位元素，并返回元素。没有定位到抛出异常
        :param loc:元素定位表达式，元组类型。
        :param msg:元素描述，用于记录到日志
        :return element
        """
        if not isinstance(loc, tuple):
            raise TypeError('loc参数类型错误，必须是元组；loc = ("id", "value1")')

        else:
            try:
                logger.info('定位{}页面元素：{}, 元素描述：{}'.format(self.page, loc, msg))
                start_time = time.time()
                ele = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(loc))
                end_time = time.time()
            except Exception:
                logger.error('元素定位失败!')
                self.save_screenshot()
                raise
            else:
                logger.info('元素定位成功：耗时{}秒!'.format(
                    round(end_time - start_time, 3)))
                return ele

    def find_elements(self, loc, msg=''):
        """
        定位元素组
        :param loc:元素定位表达式，元组类型。
        :param msg:元素描述，用于记录到日志
        :return: 元素组
        """
        if not isinstance(loc, tuple):
            raise TypeError('loc参数类型错误，必须是元组；loc = ("id", "value1")')
        else:
            try:
                logger.info('定位{}页面元素：{}, 元素描述：{}'.format(self.page, loc, msg))
                start_time = time.time()
                eles = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located(loc))
                end_time = time.time()
            except Exception:
                logger.error('元素定位失败!')
                self.save_screenshot()
                raise
            else:
                logger.info('元素定位成功：耗时{}秒!'.format(
                    round(end_time - start_time, 3)))
                return eles

    def get_handles(self):
        """
        获取当前所有句柄
        :return:所有句柄
        """
        logger.info('获取所有句柄')
        try:
            all_handles = self.driver.window_handles
        except Exception:
            logger.error('获取句柄失败')
            self.save_screenshot()
            raise
        else:
            return all_handles

    def switch_alert(self, send_keys=None):
        """
        正常获取到弹出窗的text内容就返回alert这个对象（注意这里不是返回Ture），没有获取到就返回False
        :send: 是否点击bool
        :return: alert内容
        """
        try:
            WebDriverWait(self.driver, timeout=10).until(EC.alert_is_present())
            result = self.driver.switch_to.alert
            if result and send_keys is None:
                text = result.text
                logger.info("alert出现,内容：{}".format(text))
                result.accept()
                logger.info("alert已经关闭")
                return text
            elif result and send_keys is not None:
                text = result.text
                logger.info("alert出现,内容：{}".format(text))
                result.send_key(send_keys)
                result.accept()
                logger.info("alert已经关闭")
                return text
            else:
                logger.info("未弹出alert")
        except Exception:
            logger.error("alert切换失败！")
            self.save_screenshot()
            raise

    def switch_window(self, handle='new', old_handles=None):
        """
        窗口切换==如果是切换到新窗口，new，如果是回到默认窗口，default。切换前，在新窗口打开前获取handles
        :param handle: (new, default,handle name )
        :param old_handles:切换新打开窗口时传入，传入的句柄为打开新窗口之前的所有句柄
        :return:
        """
        try:
            if handle == "new" and old_handles is not None:
                logger.info("切换到最新打开的窗口")
                WebDriverWait(self.driver,
                              10).until(EC.new_window_is_opened(old_handles))
                window_handles = self.driver.window_handles  # 获取所有窗口句柄
                self.driver.switch_to.window(window_handles[-1])
            elif handle == "default":
                logger.info("切换到第一个窗口")
                window_handles = self.driver.window_handles
                self.driver.switch_to.window(window_handles[0])
                # self.driver.switch_to_default_content()
            else:
                logger.info("切换到指定handles")
                self.driver.switch_to.window(handle)
        except Exception:
            logger.error("切换失败")
            self.save_screenshot()
            raise

    def switch_iframe(self, loc):
        """
        切换iframe
        :param loc: 元素定位
        :return:
        """
        logger.info("iframe切换：{}".format(loc))
        try:
            WebDriverWait(self.driver, timeout=10).until(
                EC.frame_to_be_available_and_switch_to_it(loc))
            logger.info("切换成功")
        except Exception:
            logger.error("iframe切换失败！")
            self.save_screenshot()
            raise

    def save_screenshot(self):
        """
        全屏截图，并加入allure报告
        :return: None
        """
        name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        filepath = BASE_DIR + r'/img/{}.png'.format(name)
        try:
            self.driver.save_screenshot(filepath)
            logger.info("截屏成功,图片路径为{}".format(filepath))
            sleep(1)
            #allure.attach.file(filepath, name, allure.attachment_type.PNG)
        except Exception:
            logger.error("截屏失败")

    def window_close(self):
        """
        关闭当前窗口
        :return:
        """
        self.driver.close()
        logger.info('关闭窗口')

    # #############元素操作部分#############

    def click(self, loc, msg=''):
        """
        点击操作
        :param loc:元素定位表达式
        :param msg:元素描述
        :return: None
        """

        try:
            logger.info('点击元素：{}'.format(msg))
            WebDriverWait(self.driver, 15).until(element_click_success(loc))
        except Exception:
            logger.error('点击失败,元素不可点击或者元素点位失败')
            self.save_screenshot()
            raise

    def click_iframe(self, loc, iframe, msg=''):
        """
        点击元素后切换iframe
        :param loc:元素定位表达式
        :param iframe:切换iframe
        :param msg:元素描述
        :return: None
        """

        try:
            logger.info('点击元素后切换iframe：{}'.format(msg))
            WebDriverWait(self.driver,
                          10).until(EC.element_to_be_clickable(loc)).click()
            self.switch_iframe(iframe)
        except Exception:
            logger.error('点击失败,元素不可点击或者元素点位失败')
            self.save_screenshot()
            raise

    def screenshot(self):
        """
        元素截图
        :return: None
        """
        name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        filepath = BASE_DIR + r'\img\{}.png'.format(name)
        try:
            self.driver.save_screenshot(filepath)
            logger.info("元素截图成功,图片路径为{}".format(filepath))
            sleep(1)
        except Exception:
            logger.error("截屏失败")

    def submit(self, loc):
        """
        提交form表单操作，元素定位在form表单中任意元素即可
        记住只能在form表单中使用，一般在submit难定位时使用
        :param loc:元素定位表达式
        :return:
        """
        ele = self.find_element(loc, msg='提交')
        try:
            logger.info('提交form表单')
            ele.submit()

        except Exception:
            logger.error('提交失败'.format())
            self.save_screenshot()
            raise

    def get_text(self, loc, msg):
        """
        获取文本内容
        :param loc: 元素定位
        :param msg: 元素描述
        :return: 文本内容
        """
        ele = self.find_element(loc, msg=msg)
        try:
            text = ele.text
            logger.info('{}元素文本：{}'.format(msg, text))
        except Exception:
            logger.error("获取文本失败")
            self.save_screenshot()
            raise
        else:
            return text

    def uncheck_checkbox(self, loc, msg=''):
        """
        取消选择复选框
        :param loc:
        :param msg:
        :return:
        """
        if self.checkbox_status(loc, msg=msg):
            self.click(loc, msg=msg)
        else:
            logger.info('复选框没有选择')

    def check_checkbox(self, loc, msg=''):
        """
        选择复选框
        :param loc:
        :param msg:
        :return:
        """
        if not self.checkbox_status(loc, msg=msg):
            self.click(loc, msg=msg)
        else:
            logger.info('复选框已是选择')

    def checkbox_status(self, loc, msg=''):
        """
        复选框状态
        :param loc:
        :param msg:
        :return:
        """
        ele = self.find_element(loc, msg=msg)
        try:
            status = ele.is_selected
            logger.info("复选框状态：{}".format(loc))
            return status
        except Exception:
            logger.error("获取复选框状态失败。")
            self.save_screenshot()
            raise

    # #############js操作部分#############
    def click_by_js(self, loc, msg=''):
        """
        点击操作
        :param loc:元素定位表达式
        :param msg:元素描述
        :return: None
        """

        try:
            logger.info('点击元素：{}'.format(msg))
            ele = WebDriverWait(self.driver,
                                10).until(EC.element_to_be_clickable(loc))
            self.driver.execute_script("arguments[0].click();", ele)
        except Exception:
            logger.error('点击失败,元素不可点击或者元素点位失败')
            self.save_screenshot()
            raise

    def removeOnly_by_js(self, loc, msg=''):
        """
        点击操作
        :param loc:元素定位表达式
        :param msg:元素描述
        :return: None
        """
        try:
            logger.info('删除{}只读属性'.format(msg))
            js = "document.getElementById('{}').removeAttribute('readOnly')".format(
                loc)
            self.driver.execute_script(js)
        except Exception:
            logger.error('删除只读属性失败')
            self.save_screenshot()
            raise

    def scroll_into_view(self, loc, msg=''):
        """
        滚动到元素可见位置
        :param loc:
        :param msg:
        :return:
        """
        ele = self.find_element(loc, msg=msg)
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(false);",
                                       ele)
            logger.info("滚动到元素：{}".format(loc))
        except Exception:
            logger.error("滚动操作失败。")
            self.save_screenshot()
            raise

    # #############鼠标操作部分#############
    def double_click(self, loc, msg=''):
        """
        鼠标双击
        :param loc: 元素定位
        :return:
        """
        ele = self.find_element(loc, msg=msg)
        try:
            AC(self.driver).double_click(ele).perform()
            logger.info("双击元素：{}".format(loc))
        except Exception:
            logger.error("鼠标双击操作失败。")
            self.save_screenshot()
            raise

    def right_click(self, loc, msg=''):
        """
        右击
        :param loc:
        :param msg:
        :return:
        """
        ele = self.find_element(loc, msg=msg)
        try:
            AC(self.driver).context_click(ele).perform()
            logger.info("右击元素：{}".format(loc))
        except Exception:
            logger.error("右击操作失败。")
            self.save_screenshot()
            raise

    def drag_and_drop(self, loc_rource, loc_tarteg, msg):
        """
        拖动元素
        :param loc_rource:
        :param loc_tarteg:
        :param msg:
        :return:
        """
        ele = self.find_element(loc_rource, msg=msg)
        ele1 = self.find_element(loc_tarteg, msg=msg)
        try:
            AC(self.driver).drag_and_drop(ele, ele1).perform()
            logger.info("拖动元素：{}，{}".format(loc_rource, loc_tarteg))
        except Exception:
            logger.error("拖动操作失败。")
            self.save_screenshot()
            raise

    def mouse_hover(self, loc, msg=''):
        """
        鼠标悬停到一个元素位置
        :param loc:
        :param msg:
        :return:
        """
        ele = self.find_element(loc, msg=msg)
        try:
            AC(self.driver).move_to_element(ele).perform()
            logger.info("鼠标悬停：{}".format(loc))
        except Exception:
            logger.error("鼠标操作失败。")
            self.save_screenshot()
            raise

    # #############键盘操作部分#############
    def key_down(self, key, text):
        """
        用于模拟按下辅助按键(CONTROL, SHIFT, ALT)的动作，按住
        :param key: 键盘操作码
        :param text:
        :return:
        """
        # Perform action ctrl + A (modifier CONTROL + Alphabet A) to select the page
        try:
            logger.info('按住{}输入{}'.format(key, text))
            AC(self.driver).key_down(key).send_keys(text).perform()
        except Exception:
            logger.error('输入失败')
            self.save_screenshot()
            raise

    def key_up(self, loc, key, text, key1, text1, msg=''):
        """
        用于模拟辅助按键(CONTROL, SHIFT, ALT)弹起或释放的操作，松开
        :param key:第一次按住键
        :param loc:定位器
        :param text:第一次输入文本
        :param key1:第二次按住的键
        :param text1:第二次输入文本
        :param msg:
        :return:
        """
        # Enters text "qwerty" with keyDown SHIFT key and after keyUp SHIFT key (QWERTYqwerty)
        ele = self.find_element(loc, msg=msg)
        try:
            logger.info('输入内容：{}{}'.format(text, text1))
            ele.clear()
            AC(self.driver).key_down(key).send_keys_to_element(
                ele, text).key_up(key1).send_keys(text1).perform()
        except Exception:
            logger.error('输入失败')
            self.save_screenshot()
            raise

    def send_keys(self, loc, text='', msg=''):
        """
        输入操作
        :param loc:元素定位表达式
        :param text: 输入内容
        :param msg:元素描述
        :return:
        """
        ele = self.find_element(loc, msg=msg)
        try:
            logger.info('输入内容：{}'.format(text))
            ele.clear()
            ele.send_keys(text)
        except Exception:
            logger.error('输入失败')
            self.save_screenshot()
            raise

    def select(self, loc, text='', msg='', types='text'):
        """

        :param loc: 元素定位表达式
        :param types: 下拉框定位方式
        :param text: 选择内容
        :param msg: 元素描述
        :return:
        """
        ele = self.find_element(loc, msg=msg)
        try:
            logger.info("下拉框操作类型：{},选择内容：{}".format(types, text))
            if types == 'text':
                SE(ele).select_by_visible_text(text)
            elif types == 'value':
                SE(ele).select_by_value(text)
            elif types == 'index':
                SE(ele).select_by_index(text)
            else:
                logger.error("不支持的操作类型")
                raise Exception('不支持的下拉框操作类型')
        except Exception:
            logger.error("下拉框内容选择失败")
            self.save_screenshot()
            raise

    def alert(self, types='accept', text=''):
        """
        :param types: 弹窗操作类型
        :param text: 输入弹窗内容
        """
        try:
            logger.info("弹窗操作类型：{},输入内容：{}".format(types, text))
            alert = self.driver.switch_to.alert
            if types == 'accept':
                if text != '':
                    alert.send_keys(text)
                alert.accept()
            elif types == 'dismiss':
                if text != '':
                    alert.send_keys(text)
                alert.dismiss()
            else:
                logger.error("不支持的操作类型")
                raise Exception('不支持的弹窗操作操作类型')
        except Exception:
            logger.error("弹窗操作失败")
            self.save_screenshot()
            raise

    # 判断元素是否存在
    def is_element_exist(self, loc, msg=''):
        """
        :param loc:元素定位表达式，元组类型。
        :param msg:元素描述，用于记录到日志
        :return
        """
        try:
            self.find_element(loc, msg)
            return True
        except:
            return False

    def quit(self):
        self.driver.quit()

    def wait_element_novisibility(self, loc, msg):
        """自动显示等待10s,定位元素不可见，并返回true。没有定位到抛出异常
                :param loc:元素定位表达式，元组类型。
                :param msg:元素描述，用于记录到日志
                :return true
                """
        if not isinstance(loc, tuple):
            raise TypeError('loc参数类型错误，必须是元组；loc = ("id", "value1")')

        else:
            try:
                logger.info('定位{}页面元素：{}, 元素描述：{}'.format(self.page, loc, msg))
                start_time = time.time()
                eles = WebDriverWait(self.driver, 15).until_not(
                    EC.visibility_of_all_elements_located(loc))
                end_time = time.time()
            except Exception:
                logger.error('元素定位失败!')
                self.save_screenshot()
                raise
            else:
                logger.info('元素定位成功：耗时{}秒!'.format(
                    round(end_time - start_time, 3)))
                return True


# 自定义的一个点击直到成功的显式等待条件
class element_click_success(object):
    """ An Expectation for checking an element is visible and enabled such that
    you can click it."""

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        try:
            element.click()
            return True
        except:
            return False
