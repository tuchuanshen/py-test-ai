# -*- coding: utf-8 -*-
# @File    : 强制解析策略配置.py
# @Author  : yq.luan
# @Date    : 2024-02-28

from selenium.webdriver.common.by import By
from basepage import BasePage


def get_params(key, update_params, **kwargs):
    return update_params.get(key) if kwargs.get(key) is None else kwargs.get(
        key)


def get_param(key, default, **kwargs):
    return default if kwargs.get(key) is None else kwargs.get(key)


class 强制解析策略配置(BasePage):
    loc_xForce下发弹窗 = (By.XPATH, '//*[@class="con"]')
    loc_xForce下发弹窗关闭 = (By.XPATH, '//*[@class="title"]/span')
    loc_xForce加载 = (By.XPATH, '//*[@id="loadingdiv"]')
    loc_xForce_iframe = (By.XPATH, '//*[@id="frame_content"]')

    loc_强制解析策略配置_筛选_源IP网段组1 = (
        By.XPATH,
        '//*[@id="selectForm"]//input[@name="forceCon.groupname"][1]')
    loc_强制解析策略配置_筛选_源IP网段组2 = (
        By.XPATH,
        '//*[@id="selectForm"]//input[@name="forceCon.groupname"][2]')
    loc_强制解析策略配置_筛选_域 = (By.XPATH, '//*[@id="filterDm"]')
    loc_强制解析策略配置_按钮_添加配置 = (By.XPATH,
                            '//*[@id="selectForm"]//input[@value="添加配置"]')
    loc_强制解析策略配置_按钮_查询 = (By.XPATH,
                          '//*[@id="selectForm"]//button[text()="查询"]')

    loc_强制解析策略配置_添加配置_源IP网段组 = (By.XPATH, '//*[@id="srcip"]')
    loc_强制解析策略配置_添加配置_请求类型 = (By.XPATH, '//*[@id="reqTypeSel"]')
    loc_强制解析策略配置_添加配置_域类型 = (By.XPATH, '//*[@id="dmtypeSel"]')
    loc_强制解析策略配置_添加配置_域 = (By.XPATH, '//*[@id="dmNameText"]')
    loc_强制解析策略配置_添加配置_解析结果 = (By.XPATH,
                              '//*[@id="addtable"]//input[@name="resipInput"]')
    loc_强制解析策略配置_添加配置_权重 = (By.XPATH,
                            '//*[@id="addtable"]//input[@name="weightInput"]')
    loc_强制解析策略配置_添加配置_TTL = (By.XPATH,
                             '//*[@id="addtable"]//input[@name="ttlInput"]')
    loc_强制解析策略配置_添加配置_确认 = (
        By.XPATH, '//*[@id="forceAddForm"]//img[@onclick="formSubmit()"]')
    loc_强制解析策略配置_列表_全选 = (By.XPATH, '//*[@id="sltAll"]')
    loc_强制解析策略配置_列表_删除 = (By.XPATH, '//*[@id="mvdiv"]//input[@value="删除"]')

    def xForce_强制解析策略配置_添加配置(self, **kwargs):
        源IP网段组 = get_param("源IP网段组", '', **kwargs)
        请求类型 = get_param("请求类型", 'A', **kwargs)
        域类型 = get_param("域类型", '域名', **kwargs)
        域 = get_param("域", '', **kwargs)
        解析结果 = get_param("解析结果", '', **kwargs)
        权重 = get_param("权重", '', **kwargs)
        TTL = get_param("TTL", '', **kwargs)
        self.click(self.loc_强制解析策略配置_按钮_添加配置, msg='强制解析策略配置_按钮_添加配置')
        if 源IP网段组:
            self.select(self.loc_强制解析策略配置_添加配置_源IP网段组,
                        源IP网段组,
                        msg='强制解析策略配置_添加配置_源IP网段组')
        self.select(self.loc_强制解析策略配置_添加配置_请求类型,
                    请求类型,
                    msg='强制解析策略配置_添加配置_请求类型')
        self.select(self.loc_强制解析策略配置_添加配置_域类型, 域类型, msg='强制解析策略配置_添加配置_域类型')
        self.send_keys(self.loc_强制解析策略配置_添加配置_域, 域, msg='强制解析策略配置_添加配置_域')
        self.send_keys(self.loc_强制解析策略配置_添加配置_解析结果,
                       解析结果,
                       msg='强制解析策略配置_添加配置_解析结果')
        self.send_keys(self.loc_强制解析策略配置_添加配置_权重, 权重, msg='强制解析策略配置_添加配置_权重')
        self.send_keys(self.loc_强制解析策略配置_添加配置_TTL,
                       TTL,
                       msg='强制解析策略配置_添加配置_TTL')
        self.click(self.loc_强制解析策略配置_添加配置_确认, msg='强制解析策略配置_添加配置_确认')
        self.click(self.loc_强制解析策略配置_按钮_查询, msg='强制解析策略配置_按钮_查询')

    def xForce_强制解析策略配置_全选删除配置(self):
        self.click(self.loc_强制解析策略配置_列表_全选, msg='强制解析策略配置_列表_全选')
        self.click(self.loc_强制解析策略配置_列表_删除, msg='强制解析策略配置_列表_删除')
        self.switch_alert()

    def xForce基本配置_加载中(self):
        result = self.is_element_exist(self.loc_xForce加载, '等待加载中状态')
        return result

    def xForce基本配置_完成加载(self):
        result = self.wait_element_novisibility(self.loc_xForce加载, '完成加载状态')
        return result

    def xForce基本配置_加载(self):
        self.driver.switch_to.default_content()
        self.xForce基本配置_加载中()
        self.xForce基本配置_完成加载()
        self.switch_iframe(self.loc_xForce_iframe)
