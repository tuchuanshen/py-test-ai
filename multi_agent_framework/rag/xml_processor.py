"""
XML数据处理模块
提供XML数据的加载和清洗功能
"""

import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional, Union
import pandas as pd
import logging
from pathlib import Path
from collections import defaultdict

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class XMLProcessor:
    """
    XML数据处理器
    提供XML数据的加载、解析和清洗功能，保留结构和元数据信息
    """

    def __init__(self):
        """初始化XML处理器"""
        self.data = None
        self.tree = None
        self.root = None

    def load_xml(self, file_path: Union[str, Path]) -> bool:
        """
        加载XML文件
        
        Args:
            file_path: XML文件路径
            
        Returns:
            bool: 加载成功返回True，失败返回False
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logger.error(f"文件不存在: {file_path}")
                return False

            # 解析XML文件
            self.tree = ET.parse(file_path)
            self.root = self.tree.getroot()
            logger.info(f"成功加载XML文件: {file_path}")
            return True

        except ET.ParseError as e:
            logger.error(f"XML解析错误: {e}")
            return False
        except Exception as e:
            logger.error(f"加载XML文件时发生错误: {e}")
            return False

    def load_xml_from_string(self, xml_string: str) -> bool:
        """
        从字符串加载XML数据
        
        Args:
            xml_string: XML格式的字符串
            
        Returns:
            bool: 加载成功返回True，失败返回False
        """
        try:
            self.root = ET.fromstring(xml_string)
            self.tree = None  # 字符串加载时没有tree对象
            logger.info("成功从字符串加载XML数据")
            return True

        except ET.ParseError as e:
            logger.error(f"XML解析错误: {e}")
            return False
        except Exception as e:
            logger.error(f"从字符串加载XML时发生错误: {e}")
            return False

    def xml_to_dict(self, element=None, preserve_structure=True) -> Dict[str, Any]:
        """
        将XML元素转换为字典格式，保留结构和元数据信息
        
        Args:
            element: XML元素，如果为None则使用根元素
            preserve_structure: 是否保留XML结构信息
            
        Returns:
            Dict: 转换后的字典
        """
        if element is None:
            element = self.root

        if element is None:
            return {}

        result: Dict[str, Any] = {}
        
        # 添加标签名作为元数据
        if preserve_structure:
            result['@tag'] = element.tag

        # 添加属性作为元数据
        if element.attrib:
            result['@attributes'] = element.attrib

        # 添加文本内容
        if element.text and element.text.strip():
            if len(element) == 0:  # 叶子节点
                result['#text'] = element.text.strip()
            else:
                result['#text'] = element.text.strip()
        elif len(element) == 0 and element.text:
            # 空白文本节点
            result['#text'] = element.text

        # 处理子元素
        children_dict = defaultdict(list)
        for child in element:
            child_data = self.xml_to_dict(child, preserve_structure)
            children_dict[child.tag].append(child_data)
        
        # 将子元素添加到结果中
        for tag, children in children_dict.items():
            if len(children) == 1:
                result[tag] = children[0]
            else:
                result[tag] = children

        return result

    def xml_to_dataframe(self, elements_path: Optional[str] = None, preserve_metadata=True) -> pd.DataFrame:
        """
        将XML数据转换为DataFrame格式，保留元数据信息
        
        Args:
            elements_path: 元素路径，指定要转换的子元素路径，如果为None则使用根元素的所有子元素
            preserve_metadata: 是否保留元数据（属性等）
            
        Returns:
            pd.DataFrame: 转换后的DataFrame
        """
        if self.root is None:
            logger.warning("XML数据未加载")
            return pd.DataFrame()

        try:
            elements = []
            if elements_path:
                target_elements = self.root.findall(elements_path)
            else:
                # 如果没有指定路径，使用根元素的所有直接子元素
                target_elements = list(self.root)

            # 将每个元素转换为字典
            for elem in target_elements:
                elem_dict = self._element_to_flat_dict(elem, preserve_metadata)
                elements.append(elem_dict)

            # 创建DataFrame
            df = pd.DataFrame(elements)
            logger.info(f"成功转换为DataFrame，共{len(df)}行")
            return df

        except Exception as e:
            logger.error(f"转换为DataFrame时发生错误: {e}")
            return pd.DataFrame()

    def _element_to_flat_dict(self, element, preserve_metadata=True) -> Dict[str, Any]:
        """
        将单个XML元素转换为扁平化的字典，可选择保留元数据
        
        Args:
            element: XML元素
            preserve_metadata: 是否保留元数据
            
        Returns:
            Dict: 转换后的字典
        """
        result: Dict[str, Any] = {}
        
        # 添加属性作为元数据列
        if preserve_metadata and element.attrib:
            for key, value in element.attrib.items():
                result[f"@{key}"] = value

        # 添加标签名作为元数据
        if preserve_metadata:
            result["@tag"] = element.tag

        # 添加文本内容
        if element.text and element.text.strip():
            result["#text"] = element.text.strip()
        elif element.text:
            result["#text"] = element.text

        # 递归处理子元素，将嵌套结构扁平化
        for child in element:
            child_dict = self._element_to_flat_dict(child, preserve_metadata)
            for key, value in child_dict.items():
                # 为子元素字段添加前缀以避免冲突
                prefixed_key = f"{child.tag}_{key}"
                # 如果键已存在，添加序号后缀
                if prefixed_key in result:
                    i = 1
                    while f"{prefixed_key}_{i}" in result:
                        i += 1
                    prefixed_key = f"{prefixed_key}_{i}"
                result[prefixed_key] = value
                    
        return result

    def clean_data(self, 
                   remove_empty_elements: bool = True,
                   remove_empty_text: bool = True,
                   strip_whitespace: bool = True,
                   remove_duplicates: bool = False,
                   preserve_structure: bool = True) -> bool:
        """
        清洗XML数据，同时保留结构和元数据信息
        
        Args:
            remove_empty_elements: 是否移除空元素
            remove_empty_text: 是否移除空文本
            strip_whitespace: 是否去除文本首尾空白
            remove_duplicates: 是否移除重复元素
            preserve_structure: 是否保留结构信息
            
        Returns:
            bool: 清洗成功返回True
        """
        if self.root is None:
            logger.warning("XML数据未加载")
            return False

        try:
            if strip_whitespace:
                self._strip_whitespace(self.root)
                
            if remove_empty_text:
                self._remove_empty_text(self.root)
                
            if remove_empty_elements:
                self._remove_empty_elements(self.root)
                
            if remove_duplicates:
                self._remove_duplicates(self.root)
                
            logger.info("数据清洗完成")
            return True

        except Exception as e:
            logger.error(f"数据清洗时发生错误: {e}")
            return False

    def _strip_whitespace(self, element):
        """去除元素文本的首尾空白"""
        if element.text:
            element.text = element.text.strip()
        if element.tail:
            element.tail = element.tail.strip()
            
        for child in element:
            self._strip_whitespace(child)

    def _remove_empty_text(self, element):
        """移除空文本"""
        if element.text and not element.text.strip():
            element.text = None
        if element.tail and not element.tail.strip():
            element.tail = None
            
        for child in element:
            self._remove_empty_text(child)

    def _remove_empty_elements(self, element):
        """移除空元素"""
        children_to_remove = []
        for child in element:
            # 递归处理子元素
            self._remove_empty_elements(child)
            
            # 检查是否为空元素（无文本、无属性、无子元素）
            if (not child.text or not child.text.strip()) and \
               not child.attrib and \
               len(child) == 0:
                children_to_remove.append(child)
                
        for child in children_to_remove:
            element.remove(child)

    def _remove_duplicates(self, element):
        """移除重复元素（简化版）"""
        seen = {}
        children_to_remove = []
        
        for child in element:
            # 创建元素的唯一标识（标签名+属性）
            element_id = (child.tag, tuple(sorted(child.attrib.items())))
            
            if element_id in seen:
                children_to_remove.append(child)
            else:
                seen[element_id] = child
                
        for child in children_to_remove:
            element.remove(child)
            
        # 递归处理剩余的子元素
        for child in element:
            self._remove_duplicates(child)

    def extract_structured_content(self, element=None) -> List[Dict[str, Any]]:
        """
        提取结构化内容，保留标签结构和元数据信息
        
        Args:
            element: XML元素，如果为None则使用根元素
            
        Returns:
            List[Dict]: 结构化内容列表
        """
        if element is None:
            element = self.root
            
        if element is None:
            return []
            
        content_list = []
        self._extract_content_recursive(element, content_list, path=[])
        return content_list

    def _extract_content_recursive(self, element, content_list, path):
        """
        递归提取内容，保留结构信息
        
        Args:
            element: 当前处理的XML元素
            content_list: 存储提取内容的列表
            path: 当前元素在XML树中的路径
        """
        # 构建当前路径
        current_path = path + [element.tag]
        
        # 创建内容项
        content_item = {
            'path': '/'.join(current_path),
            'tag': element.tag,
            'attributes': element.attrib if element.attrib else {},
            'text': element.text.strip() if element.text and element.text.strip() else None
        }
        
        # 只有当元素有文本内容或属性时才添加到结果中
        if content_item['text'] or content_item['attributes']:
            content_list.append(content_item)
            
        # 递归处理子元素
        for child in element:
            self._extract_content_recursive(child, content_list, current_path)

    def get_element_by_path(self, path: str) -> Optional[ET.Element]:
        """
        根据路径获取元素
        
        Args:
            path: XPath路径
            
        Returns:
            Optional[ET.Element]: 找到的元素，未找到返回None
        """
        if self.root is None:
            return None
            
        try:
            return self.root.find(path)
        except Exception as e:
            logger.error(f"查找元素时发生错误: {e}")
            return None

    def get_elements_by_path(self, path: str) -> List[ET.Element]:
        """
        根据路径获取多个元素
        
        Args:
            path: XPath路径
            
        Returns:
            List[ET.Element]: 找到的元素列表
        """
        if self.root is None:
            return []
            
        try:
            return self.root.findall(path)
        except Exception as e:
            logger.error(f"查找元素时发生错误: {e}")
            return []

    def save_xml(self, file_path: Union[str, Path], encoding: str = 'utf-8') -> bool:
        """
        保存XML到文件
        
        Args:
            file_path: 保存路径
            encoding: 编码格式
            
        Returns:
            bool: 保存成功返回True
        """
        if self.tree is None and self.root is None:
            logger.warning("没有可保存的XML数据")
            return False

        try:
            file_path = Path(file_path)
            
            # 确保目录存在
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 如果有tree对象，使用tree保存（保留格式）
            if self.tree is not None:
                self.tree.write(file_path, encoding=encoding, xml_declaration=True)
            else:
                # 否则直接保存root
                tree = ET.ElementTree(self.root)
                tree.write(file_path, encoding=encoding, xml_declaration=True)
                
            logger.info(f"XML文件保存成功: {file_path}")
            return True

        except Exception as e:
            logger.error(f"保存XML文件时发生错误: {e}")
            return False


def load_xml_data(file_path: Union[str, Path], preserve_structure=True) -> Optional[Dict[str, Any]]:
    """
    加载XML数据并转换为字典格式的便捷函数
    
    Args:
        file_path: XML文件路径
        preserve_structure: 是否保留结构信息
        
    Returns:
        Optional[Dict]: 转换后的字典数据，失败返回None
    """
    processor = XMLProcessor()
    if processor.load_xml(file_path):
        return processor.xml_to_dict(preserve_structure=preserve_structure)
    return None


def clean_xml_data(file_path: Union[str, Path], 
                   output_path: Optional[Union[str, Path]] = None,
                   **clean_options) -> bool:
    """
    清洗XML数据的便捷函数
    
    Args:
        file_path: 输入XML文件路径
        output_path: 输出XML文件路径，如果为None则覆盖原文件
        **clean_options: 清洗选项
        
    Returns:
        bool: 清洗成功返回True
    """
    processor = XMLProcessor()
    if not processor.load_xml(file_path):
        return False
        
    if not processor.clean_data(**clean_options):
        return False
        
    save_path = output_path if output_path else file_path
    return processor.save_xml(save_path)


# 使用示例
if __name__ == "__main__":
    # 示例XML数据
    sample_xml = """
    <root>
        <section number="1" type="introduction">
            <title>简介</title>
            <t>这是文档的第一部分。</t>
            <t>包含一些基本概念。</t>
        </section>
        <section number="2" type="main">
            <title>主要内容</title>
            <t>这是文档的核心部分。</t>
            <figure id="fig1">
                <title>示例图</title>
                <t>这是一个示例图。</t>
            </figure>
            <list type="ordered">
                <t>第一项</t>
                <t>第二项</t>
                <t>第三项</t>
            </list>
        </section>
    </root>
    """
    
    # 创建处理器实例
    processor = XMLProcessor()
    
    # 从字符串加载XML
    if processor.load_xml_from_string(sample_xml):
        print("XML数据加载成功")
        
        # 转换为字典，保留结构和元数据
        data_dict = processor.xml_to_dict(preserve_structure=True)
        print("字典格式数据（保留结构）:")
        print(data_dict)
        
        # 提取结构化内容
        structured_content = processor.extract_structured_content()
        print("\n结构化内容:")
        for item in structured_content:
            print(f"  路径: {item['path']}")
            print(f"  标签: {item['tag']}")
            print(f"  属性: {item['attributes']}")
            print(f"  文本: {item['text']}")
            print()
        
        # 转换为DataFrame
        df = processor.xml_to_dataframe(preserve_metadata=True)
        print("DataFrame格式数据:")
        print(df)
        
        # 清洗数据
        processor.clean_data(preserve_structure=True)
        print("\n数据清洗完成")
        
        # 保存到文件
        processor.save_xml("sample_output.xml")
        print("数据已保存到sample_output.xml")