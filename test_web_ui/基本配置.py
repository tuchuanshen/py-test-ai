# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from basepage import BasePage
import time


class 基本配置(BasePage):

    loc_xForce下发弹窗 = (By.XPATH, '//*[@class="con"]')
    loc_xForce下发弹窗关闭 = (By.XPATH, '//*[@class="title"]/span')
    loc_xForce加载 = (By.XPATH, '//*[@id="loadingdiv"]')
    loc_xForce_iframe = (By.XPATH, '//*[@id="frame_content"]')

    loc_强制解析功能模块开关 = (By.XPATH, '//*[@id="22310001"]//input[@value="切换"]')
    loc_强制解析功能模块开关_状态 = (By.XPATH, '//*[@id="22310001"]//td[@align]/span')

    loc_灰色域名劫持功能模块开关 = (By.XPATH, '//*[@id="22310002"]//input[@value="切换"]')
    loc_灰色域名劫持功能模块开关_状态 = (By.XPATH, '//*[@id="22310002"]//td[@align]/span')
    loc_灰色域名劫持限速 = (By.XPATH, '//*[@id="hijackText"]')
    loc_灰色域名劫持限速设定 = (By.XPATH, '//*[@id="22310002"]//input[@value="设定"]')

    loc_资源总线功能模块开关 = (By.XPATH, '//*[@id="22310003"]//input[@value="切换"]')
    loc_资源总线功能模块开关_状态 = (By.XPATH, '//*[@id="22310003"]//td[@align]/span')

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

    def xForce基本配置_强制解析功能模块开关_状态(self):
        result = self.get_text(self.loc_强制解析功能模块开关_状态, '强制解析功能模块开关_状态')
        return result

    def xForce基本配置_强制解析功能模块开关(self):
        self.click(self.loc_强制解析功能模块开关, '点击强制解析功能模块开关')
        self.xForce基本配置_加载()

    def xForce基本配置_弹窗(self):
        result = self.get_text(self.loc_xForce下发弹窗, 'loc_xForce下发弹窗')
        self.click(self.loc_xForce下发弹窗关闭, msg='关闭下发弹窗')
        return result

    def xForce基本配置_弹窗_关闭(self):
        self.click(self.loc_xForce下发弹窗关闭, msg='关闭弹窗')

    def xForce基本配置_灰色域名劫持功能模块开关_状态(self):
        result = self.get_text(self.loc_灰色域名劫持功能模块开关_状态, '灰色域名劫持功能模块开关_状态')
        return result

    def xForce基本配置_灰色域名劫持功能模块开关(self):
        self.click(self.loc_灰色域名劫持功能模块开关, '点击灰色域名劫持功能模块开关')
        # self.xForce基本配置_加载()

    def xForce基本配置_灰色域名劫持限速_input_true(self, text):
        self.send_keys(self.loc_灰色域名劫持限速, text, '输入灰色域名劫持限速')
        self.click(self.loc_灰色域名劫持限速设定, '点击灰色域名劫持限速设定')
        self.xForce基本配置_加载()

    def xForce基本配置_灰色域名劫持限速_input_false(self, text):
        self.send_keys(self.loc_灰色域名劫持限速, text, '输入灰色域名劫持限速')
        self.click(self.loc_灰色域名劫持限速设定, '点击灰色域名劫持限速设定')
        result = self.switch_alert()
        return result

    def xForce基本配置_资源总线功能模块开关_状态(self):
        result = self.get_text(self.loc_资源总线功能模块开关_状态, '资源总线功能模块开关_状态')
        return result

    def xForce基本配置_资源总线功能模块开关(self):
        self.click(self.loc_资源总线功能模块开关, '点击资源总线功能模块开关')
        self.xForce基本配置_加载()

    def xForce基本配置_强制解析功能模块开关_切换(self, 状态):
        if self.get_text(self.loc_强制解析功能模块开关_状态, '获取强制解析功能模块状态') != '状态：' + 状态:
            self.click(self.loc_强制解析功能模块开关, msg='切换强制解析功能模块开关')

    def xForce基本配置_灰色域名劫持功能模块开关_切换(self, 状态):
        if self.get_text(self.loc_灰色域名劫持功能模块开关_状态,
                         '获取灰色域名劫持功能模块状态') != '状态：' + 状态:
            self.click(self.loc_灰色域名劫持功能模块开关, msg='切换灰色域名劫持功能模块开关')
