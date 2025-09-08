# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By

from 基本配置 import 基本配置
from 强制解析策略配置 import 强制解析策略配置
import ipaddress
import datetime

# 选择协议栈，今天的日期是偶数时执行Ipv4,奇数执行Ipv6
PROTOCOL = "ipv4" if int(
    datetime.date.today().strftime('%d')) % 2 == 0 else "ipv6"


class xForce配置(基本配置, 强制解析策略配置):

    def __init__(self, conf):
        super(xForce配置, self).__init__(conf)


class 业务配置(xForce配置):

    def __init__(self, driver):
        super(业务配置, self).__init__(driver)


class UiOperation(业务配置):

    def __init__(self, driver):
        super(UiOperation, self).__init__(driver)

    loc_用户名 = (By.XPATH, '//*[@id="uname"]')
    loc_密码 = (By.XPATH, '//*[@id="pwd"]')
    loc_验证码 = (By.XPATH, '//*[@id="vldCode"]')
    loc_提交 = (By.XPATH, '//*[@id="loginin"]')

    # 一级菜单
    loc_首页 = (By.XPATH, '/html//div[text()="首页"]')
    loc_配置管理 = (By.XPATH, '/html//div[text()="配置管理"]')
    loc_告警管理 = (By.XPATH, '/html//div[text()="告警管理"]')
    loc_报表管理 = (By.XPATH, '/html//div[text()="报表管理"]')
    loc_DNS工具 = (By.XPATH, '/html//div[text()="DNS工具"]')
    loc_系统管理 = (By.XPATH, '/html//div[text()="系统管理"]')
    loc_快捷功能 = (By.XPATH, '/html//div[text()="快捷功能"]')

    loc_红色告警 = (By.XPATH, '//*[@id="redbtn"]')
    loc_橙色告警 = (By.XPATH, '//*[@id="orangebtn"]')
    loc_黄色告警 = (By.XPATH, '//*[@id="yellowbtn"]')

    loc_返回 = (By.XPATH, '/html//span[text()="返回"]')
    loc_个人信息 = (By.XPATH, '/html//span[text()="个人信息"]')
    loc_修改密码 = (By.XPATH, '/html//span[text()="修改密码"]')
    loc_返回 = (By.XPATH, '/html//span[text()="退出"]')

    # 二级菜单 配置管理
    loc_资源配置 = (By.XPATH, '/html//div[text()="资产配置"]')
    loc_业务配置 = (By.XPATH, '/html//div[text()="业务配置"]')
    loc_递归配置 = (By.XPATH, '/html//div[text()="递归配置"]')

    # 三级菜单 配置管理->业务配置
    loc_SecurePro配置 = (By.XPATH, '//*[@id="mymenutree_221000_clk"]')
    loc_EDNS配置 = (By.XPATH, '//*[@id="mymenutree_225000_clk"]')
    loc_CachePro配置 = (By.XPATH, '//*[@id="mymenutree_222000_clk"]')
    loc_xForce配置 = (By.XPATH, '//*[@id="mymenutree_223000_clk"]')
    loc_SmartEcho配置 = (By.XPATH, '//*[@id="mymenutree_224000_clk"]')
    loc_SpreadECHO配置 = (By.XPATH, '//*[@id="mymenutree_226200_clk"]')
    loc_xProxy配置 = (By.XPATH, '//*[@id="mymenutree_227000_clk"]')
    loc_CacheMV配置 = (By.XPATH, '//*[@id="mymenutree_222600_clk"]')
    loc_xForward策略配置 = (By.XPATH, '//*[@id="mymenutree_222900_clk"]')
    loc_FlowExport配置 = (By.XPATH, '//*[@id="mymenutree_228000_clk"]')
    loc_第三方接口管理 = (By.XPATH, '//*[@id="mymenutree_2221000_clk"]')

    # 四级菜单 配置管理->业务配置->SecurePro配置
    loc_SecurePro配置_基本配置 = (By.XPATH,
                            '//*[@id="mymenutree_221100_nodeclick_vl"]')
    loc_SecurePro配置_源IP段限速配置 = (By.XPATH,
                                '//*[@id="mymenutree_221600_nodeclick_vl"]')
    loc_SecurePro配置_用户IP段配置 = (By.XPATH,
                               '//*[@id="mymenutree_221300_nodeclick_vl"]')
    loc_SecurePro配置_业务IP配置 = (By.XPATH,
                              '//*[@id="mymenutree_221400_nodeclick_vl"]')
    loc_SecurePro配置_高级ACL配置 = (By.XPATH,
                               '//*[@id="mymenutree_221500_nodeclick_vl"]')
    loc_SecurePro配置_域限速配置 = (By.XPATH,
                             '//*[@id="mymenutree_221700_nodeclick_vl"]')
    loc_SecurePro配置_工作模式切换 = (By.XPATH,
                              '//*[@id="mymenutree_221900_nodeclick_vl"]')
    loc_SecurePro配置_重点域名保障 = (By.XPATH, '//*[@id="mymenutree_221910_clk"]')
    loc_SecurePro配置_授信域名策略配置 = (By.XPATH, '//*[@id="mymenutree_226000_clk"]')

    # 五级菜单 配置管理->业务配置->SecurePro配置->重点域名保障
    loc_SecurePro配置_重点域名保障_重点域名应答保障 = (
        By.XPATH, '//*[@id="mymenutree_221913_nodeclick_vl"]')
    loc_SecurePro配置_重点域名保障_重点域名监控告警 = (
        By.XPATH, '//*[@id="mymenutree_221911_nodeclick_vl"]')
    loc_SecurePro配置_重点域名保障_重点域名解析保障 = (
        By.XPATH, '//*[@id="mymenutree_221912_nodeclick_vl"]')
    loc_SecurePro配置_重点域名保障_重点域名安全保障 = (
        By.XPATH, '//*[@id="mymenutree_221914_nodeclick_vl"]')
    loc_SecurePro配置_重点域名保障_拨测参数配置 = (
        By.XPATH, '//*[@id="mymenutree_221915_nodeclick_vl"]')
    loc_SecurePro配置_重点域名保障_重点域名拨测历史 = (
        By.XPATH, '//*[@id="mymenutree_221916_nodeclick_vl"]')

    # 五级菜单 配置管理->业务配置->SecurePro配置->授信域名策略配置
    loc_SecurePro配置_授信域名策略配置_基本配置 = (
        By.XPATH, '//*[@id="mymenutree_226100_nodeclick_vl"]')
    loc_SecurePro配置_授信域名策略配置_授信域名列表 = (
        By.XPATH, '//*[@id="mymenutree_221800_nodeclick_vl"]')
    loc_SecurePro配置_授信域名策略配置_非授信域名策略 = (
        By.XPATH, '//*[@id="mymenutree_221110_nodeclick_vl"]')

    # 四级菜单 配置管理->业务配置->EDNS配置
    loc_EDNS配置_基本配置 = (By.XPATH, '//*[@id="mymenutree_225100_nodeclick_vl"]')
    loc_EDNS配置_用户源地址组配置 = (By.XPATH,
                           '//*[@id="mymenutree_225600_nodeclick_vl"]')
    loc_EDNS配置_EDNS源地址组下发配置 = (By.XPATH,
                               '//*[@id="mymenutree_261200_nodeclick_vl"]')
    loc_EDNS配置_服务器组配置 = (By.XPATH, '//*[@id="mymenutree_225200_nodeclick_vl"]')
    loc_EDNS配置_EDNS业务数据配置 = (By.XPATH,
                             '//*[@id="mymenutree_225700_nodeclick_vl"]')
    loc_EDNS配置_EDNS递归域名配置 = (By.XPATH,
                             '//*[@id="mymenutree_225800_nodeclick_vl"]')
    loc_EDNS配置_EDNS递归NS白名单配置 = (By.XPATH,
                                '//*[@id="mymenutree_225900_nodeclick_vl"]')

    # 四级菜单 配置管理->业务配置->CachePro配置
    loc_CachePro配置_基本配置 = (By.XPATH,
                           '//*[@id="mymenutree_222100_nodeclick_vl"]')
    loc_CachePro配置_域TTL配置 = (By.XPATH,
                             '//*[@id="mymenutree_222200_nodeclick_vl"]')
    loc_CachePro配置_缓存禁用IP段配置 = (By.XPATH,
                                '//*[@id="mymenutree_222300_nodeclick_vl"]')
    loc_CachePro配置_缓存禁用域配置 = (By.XPATH,
                              '//*[@id="mymenutree_222400_nodeclick_vl"]')
    loc_CachePro配置_后端禁用IP段配置 = (By.XPATH,
                                '//*[@id="mymenutree_222500_nodeclick_vl"]')

    # 四级菜单 配置管理->业务配置->xForce配置
    loc_xForce配置_基本配置 = (By.XPATH, '//*[@id="mymenutree_223100"]')
    loc_xForce配置_强制解析 = (By.XPATH, '//*[@id="mymenutree_223200_clk"]')
    loc_xForce配置_灰色域名劫持 = (By.XPATH, '//*[@id="mymenutree_223300_clk"]')
    loc_xForce配置_智能引流 = (By.XPATH, '//*[@id="mymenutree_223400_clk"]')

    # 五级菜单 配置管理->业务配置->xForce配置->强制解析
    loc_xForce配置_强制解析_源IP段配置 = (By.XPATH,
                                '//*[@id="mymenutree_223210_nodeclick_vl"]')
    loc_xForce配置_强制解析_强制解析策略配置 = (By.XPATH,
                                  '//*[@id="mymenutree_223220_nodeclick_vl"]')
    loc_xForce配置_强制解析_IPTV_DNS = (By.XPATH,
                                  '//*[@id="mymenutree_223270_nodeclick_vl"]')
    loc_xForce配置_强制解析_IMS_DNS = (By.XPATH,
                                 '//*[@id="mymenutree_223280_nodeclick_vl"]')
    loc_xForce配置_强制解析_ITMS_DNS = (By.XPATH,
                                  '//*[@id="mymenutree_223290_nodeclick_vl"]')

    # 五级菜单 配置管理->业务配置->xForce配置->灰色域名劫持
    loc_xForce配置_灰色域名劫持_劫持IP配置 = (By.XPATH,
                                  '//*[@id="mymenutree_223320_nodeclick_vl"]')
    loc_xForce配置_灰色域名劫持_劫持域配置 = (By.XPATH,
                                 '//*[@id="mymenutree_223330_nodeclick_vl"]')
    loc_xForce配置_灰色域名劫持_IP段黑名单 = (By.XPATH,
                                  '//*[@id="mymenutree_223340_nodeclick_vl"]')
    loc_xForce配置_灰色域名劫持_域黑名单 = (By.XPATH,
                                '//*[@id="mymenutree_223350_nodeclick_vl"]')

    # 五级菜单 配置管理->业务配置->xForce配置->智能引流
    loc_xForce配置_智能引流_策略域名 = (By.XPATH,
                              '//*[@id="mymenutree_223410_nodeclick_vl"]')
    loc_xForce配置_智能引流_开户信息 = (By.XPATH,
                              '//*[@id="mymenutree_223420_nodeclick_vl"]')
    loc_xForce配置_智能引流_上线信息 = (By.XPATH,
                              '//*[@id="mymenutree_223430_nodeclick_vl"]')

    # 四级菜单 配置管理->业务配置->SmartEcho配置
    loc_SmartEcho配置_基本配置 = (By.XPATH,
                            '//*[@id="mymenutree_224010_nodeclick_vl"]')
    loc_SmartEcho配置_解析结果黑名单策略 = (By.XPATH,
                                 '//*[@id="mymenutree_224180_nodeclick_vl"]')
    loc_SmartEcho配置_智能解析 = (By.XPATH, '//*[@id="mymenutree_224100_clk"]')
    loc_SmartEcho配置_NXR配置 = (By.XPATH, '//*[@id="mymenutree_224200_clk"]')

    # 五级菜单 配置管理->业务配置->SmartEcho配置->智能解析
    loc_SmartEcho配置_智能解析_源IP段配置 = (By.XPATH,
                                   '//*[@id="mymenutree_224130_nodeclick_vl"]')
    loc_SmartEcho配置_智能解析_源IP段黑名单配置 = (
        By.XPATH, '//*[@id="mymenutree_224160_nodeclick_vl"]')
    loc_SmartEcho配置_智能解析_解析IP段配置 = (
        By.XPATH, '//*[@id="mymenutree_224140_nodeclick_vl"]')
    loc_SmartEcho配置_智能解析_智能解析策略配置 = (
        By.XPATH, '//*[@id="mymenutree_224150_nodeclick_vl"]')
    loc_SmartEcho配置_智能解析_域黑名单配置 = (By.XPATH,
                                   '//*[@id="mymenutree_224170_nodeclick_vl"]')

    # 五级菜单 配置管理->业务配置->SmartEcho配置->NXR配置
    loc_SmartEcho配置_NXR配置_重定向IP配置 = (
        By.XPATH, '//*[@id="mymenutree_224220_nodeclick_vl"]')
    loc_SmartEcho配置_NXR配置_IP段黑名单 = (
        By.XPATH, '//*[@id="mymenutree_224230_nodeclick_vl"]')
    loc_SmartEcho配置_NXR配置_域黑名单 = (By.XPATH,
                                  '//*[@id="mymenutree_224240_nodeclick_vl"]')

    # 四级菜单 配置管理->业务配置->SpreadECHO配置
    loc_SpreadECHO配置_基本配置 = (By.XPATH,
                             '//*[@id="mymenutree_226300_nodeclick_vl"]')
    loc_SpreadECHO配置_异网业务IP黑名单 = (By.XPATH,
                                  '//*[@id="mymenutree_221710_nodeclick_vl"]')
    loc_SpreadECHO配置_异网源IP黑名单 = (By.XPATH,
                                 '//*[@id="mymenutree_221720_nodeclick_vl"]')
    loc_SpreadECHO配置_异网域黑名单 = (By.XPATH,
                               '//*[@id="mymenutree_221730_nodeclick_vl"]')

    # 四级菜单 配置管理->业务配置->xProxy配置
    loc_xProxy配置_基本配置 = (By.XPATH, '//*[@id="mymenutree_227100_nodeclick_vl"]')
    loc_xProxy配置_源IP段配置 = (By.XPATH,
                           '//*[@id="mymenutree_227200_nodeclick_vl"]')
    loc_xProxy配置_服务器组配置 = (By.XPATH,
                           '//*[@id="mymenutree_227400_nodeclick_vl"]')
    loc_xProxy配置_策略配置 = (By.XPATH, '//*[@id="mymenutree_227500_nodeclick_vl"]')
    loc_xProxy配置_IP段黑名单 = (By.XPATH,
                           '//*[@id="mymenutree_227700_nodeclick_vl"]')
    loc_xProxy配置_域黑名单 = (By.XPATH, '//*[@id="mymenutree_227800_nodeclick_vl"]')

    # 四级菜单 配置管理->业务配置->CacheMV配置 *
    #######  这边会根据安装的选项会有不同的展示形式 ######
    loc_CacheMV配置_基本配置 = (By.XPATH,
                          '//*[@id="mymenutree_222610_nodeclick_vl"]')
    loc_CacheMV配置_缓存视图源IP段配置 = (By.XPATH,
                                '//*[@id="mymenutree_222620_nodeclick_vl"]')
    loc_CacheMV配置_缓存视图策略配置 = (By.XPATH,
                              '//*[@id="mymenutree_222630_nodeclick_vl"]')

    # 四级菜单 配置管理->业务配置->xForward策略配置
    loc_xForward策略配置_递归服务器配置 = (By.XPATH,
                                '//*[@id="mymenutree_222910_nodeclick_vl"]')
    loc_xForward策略配置_域名合并配置 = (By.XPATH,
                               '//*[@id="mymenutree_222920_nodeclick_vl"]')
    loc_xForward策略配置_域名镜像配置 = (By.XPATH,
                               '//*[@id="mymenutree_222930_nodeclick_vl"]')
    loc_xForward策略配置_域名轮询配置 = (By.XPATH,
                               '//*[@id="mymenutree_222940_nodeclick_vl"]')

    # 四级菜单 配置管理->业务配置->FlowExport配置
    loc_FlowExport配置_实时统计配置 = (By.XPATH, '//*[@id="mymenutree_228100_clk"]')

    # 五级菜单 配置管理->业务配置->FlowExport配置->实时统计配置
    loc_FlowExport配置_实时统计配置_策略域配置 = (
        By.XPATH, '//*[@id="mymenutree_228110_nodeclick_vl"]')
    loc_FlowExport配置_实时统计配置_策略域名配置 = (
        By.XPATH, '//*[@id="mymenutree_228120_nodeclick_vl"]')
    loc_FlowExport配置_实时统计配置_策略IP配置 = (
        By.XPATH, '//*[@id="mymenutree_228130_nodeclick_vl"]')
    loc_FlowExport配置_实时统计配置_策略IP段配置 = (
        By.XPATH, '//*[@id="mymenutree_228140_nodeclick_vl"]')

    # 四级菜单 配置管理->业务配置->第三方接口管理
    loc_第三方接口管理_基本配置 = (By.XPATH, '//*[@id="mymenutree_2221600_nodeclick_vl"]')
    loc_第三方接口管理_域名监管XGJ = (By.XPATH,
                           '//*[@id="mymenutree_2221100_nodeclick_vl"]')
    loc_第三方接口管理_域名保障WAJ = (By.XPATH,
                           '//*[@id="mymenutree_2221200_nodeclick_vl"]')
    loc_第三方接口管理_域名信安ISMS = (By.XPATH,
                            '//*[@id="mymenutree_2221300_nodeclick_vl"]')
    loc_第三方接口管理_移动集团抗D指令 = (By.XPATH,
                            '//*[@id="mymenutree_2221350_nodeclick_vl"]')
    loc_第三方接口管理_移动集团总部运营 = (By.XPATH,
                            '//*[@id="mymenutree_2221360_nodeclick_vl"]')
    loc_第三方接口管理_域名白名单 = (By.XPATH,
                         '//*[@id="mymenutree_2221400_nodeclick_vl"]')
    loc_第三方接口管理_接口下发任务 = (By.XPATH,
                          '//*[@id="mymenutree_2221500_nodeclick_vl"]')
    loc_第三方接口管理_接口下发策略 = (By.XPATH,
                          '//*[@id="mymenutree_2221550_nodeclick_vl"]')

    loc_iframe = (By.XPATH, '//*[@id="frame_content"]')

    loc_系统 = (By.XPATH, '//*[@id="root"]//span[text()="系统"]')

    def open_配置管理(self):
        self.click(self.loc_配置管理, '进入配置管理菜单')

    def open_业务配置(self):
        self.click(self.loc_业务配置, '进入业务配置菜单')

    def exit_iframe(self):
        self.driver.switch_to.default_content()

    def open_SecurePro配置(self):
        self.click(self.loc_SecurePro配置, '进入SecurePro配置菜单')

    def open_SecurePro配置_基本配置(self):
        self.click_iframe(self.loc_SecurePro配置_基本配置, self.loc_iframe,
                          '进入SecurePro配置菜单_基本配置菜单')

    def open_SecurePro配置_用户IP段配置(self):
        self.click_iframe(self.loc_SecurePro配置_用户IP段配置, self.loc_iframe,
                          '进入SecurePro配置菜单_用户IP段配置菜单')

    def open_SecurePro配置_源IP段限速配置(self):
        self.click_iframe(self.loc_SecurePro配置_源IP段限速配置, self.loc_iframe,
                          '进入SecurePro配置菜单_源IP段限速配置菜单')

    def open_SecurePro配置_业务IP配置(self):
        self.click_iframe(self.loc_SecurePro配置_业务IP配置, self.loc_iframe,
                          '进入SecurePro配置菜单_业务IP配置菜单')

    def open_SecurePro配置_高级ACL配置(self):
        self.click_iframe(self.loc_SecurePro配置_高级ACL配置, self.loc_iframe,
                          '进入SecurePro配置菜单_高级ACL配置菜单')

    def open_SecurePro配置_域限速配置(self):
        self.click_iframe(self.loc_SecurePro配置_域限速配置, self.loc_iframe,
                          '进入SecurePro配置菜单_域限速配置菜单')

    def open_SecurePro配置_工作模式切换(self):
        self.click_iframe(self.loc_SecurePro配置_工作模式切换, self.loc_iframe,
                          '进入SecurePro配置菜单_工作模式切换菜单')

    def open_SecurePro配置_重点域名保障(self):
        self.click(self.loc_SecurePro配置_重点域名保障, '进入SecurePro配置菜单_重点域名保障菜单')

    def open_SecurePro配置_授信域名策略配置(self):
        self.click_iframe(self.loc_SecurePro配置_授信域名策略配置, self.loc_iframe,
                          '进入SecurePro配置菜单_授信域名策略配置菜单')

    def open_SecurePro配置_重点域名保障_重点域名应答保障(self):
        self.click_iframe(self.loc_SecurePro配置_重点域名保障_重点域名应答保障,
                          self.loc_iframe, "进入SecurePro配置菜单_重点域名应答保障菜单")

    def open_SecurePro配置_重点域名保障_重点域名监控告警(self):
        self.click_iframe(self.loc_SecurePro配置_重点域名保障_重点域名监控告警,
                          self.loc_iframe, "进入SecurePro配置菜单_重点域名监控告警菜单")

    def open_SecurePro配置_重点域名保障_重点域名解析保障(self):
        self.click_iframe(self.loc_SecurePro配置_重点域名保障_重点域名解析保障,
                          self.loc_iframe, "进入SecurePro配置菜单_重点域名解析保障菜单")

    def open_SecurePro配置_重点域名保障_重点域名安全保障(self):
        self.click_iframe(self.loc_SecurePro配置_重点域名保障_重点域名安全保障,
                          self.loc_iframe, "进入SecurePro配置菜单_重点域名安全保障菜单")

    def open_SecurePro配置_重点域名保障_拨测参数配置(self):
        self.click_iframe(self.loc_SecurePro配置_重点域名保障_拨测参数配置, self.loc_iframe,
                          "进入SecurePro配置菜单_拨测参数配置菜单")

    def open_SecurePro配置_重点域名保障_重点域名拨测历史(self):
        self.click_iframe(self.loc_SecurePro配置_重点域名保障_重点域名拨测历史,
                          self.loc_iframe, "进入SecurePro配置菜单_重点域名拨测历史菜单")

    def open_CachePro配置(self):
        self.click(self.loc_CachePro配置, '进入CachePro配置菜单')

    def open_CachePro配置_基本配置(self):
        self.click_iframe(self.loc_CachePro配置_基本配置, self.loc_iframe,
                          '进入CachePro配置菜单_基本配置菜单')

    def open_CachePro配置_域TTL配置(self):
        self.click_iframe(self.loc_CachePro配置_域TTL配置, self.loc_iframe,
                          '进入CachePro配置菜单_域TTL配置菜单')

    def open_CachePro配置_缓存禁用IP段配置(self):
        self.click_iframe(self.loc_CachePro配置_缓存禁用IP段配置, self.loc_iframe,
                          '进入CachePro配置菜单_缓存禁用IP段配置菜单')

    def open_CachePro配置_缓存禁用域配置(self):
        self.click_iframe(self.loc_CachePro配置_缓存禁用域配置, self.loc_iframe,
                          '进入CachePro配置菜单_缓存禁用域配置菜单')

    def open_CachePro配置_后端禁用IP段配置(self):
        self.click_iframe(self.loc_CachePro配置_后端禁用IP段配置, self.loc_iframe,
                          '进入CachePro配置菜单_后端禁用IP段配置菜单')

    def open_xForce配置(self):
        self.click(self.loc_xForce配置, '进入xForce配置菜单')

    def open_xForce配置_基本配置(self):
        self.click_iframe(self.loc_xForce配置_基本配置, self.loc_iframe,
                          '进入xForce配置菜单_基本配置菜单')

    def open_xForce配置_强制解析(self):
        self.click(self.loc_xForce配置_强制解析, '进入xForce配置_xForce配置_强制解析菜单')

    def open_xForce配置_强制解析_源IP段配置(self):
        self.click_iframe(self.loc_xForce配置_强制解析_源IP段配置, self.loc_iframe,
                          '进入xForce配置_xForce配置_强制解析_源IP段配置菜单')

    def open_xForce配置_强制解析_强制解析策略配置(self):
        self.click_iframe(self.loc_xForce配置_强制解析_强制解析策略配置, self.loc_iframe,
                          '进入xForce配置_xForce配置_强制解析_强制解析策略配置菜单')

    def open_xForce配置_灰色域名劫持(self):
        self.click(self.loc_xForce配置_灰色域名劫持, '进入xForce配置_灰色域名劫持菜单')

    def open_xForce配置_灰色域名劫持_劫持IP配置(self):
        self.click_iframe(self.loc_xForce配置_灰色域名劫持_劫持IP配置, self.loc_iframe,
                          '进入xForce配置__灰色域名劫持_劫持IP配置菜单')

    def open_xForce配置_灰色域名劫持_劫持域配置(self):
        self.click_iframe(self.loc_xForce配置_灰色域名劫持_劫持域配置, self.loc_iframe,
                          '进入xForce配置__灰色域名劫持_劫持域配置菜单')

    def open_xForce配置_灰色域名劫持_IP段黑名单(self):
        self.click_iframe(self.loc_xForce配置_灰色域名劫持_IP段黑名单, self.loc_iframe,
                          '进入xForce配置__灰色域名劫持_IP段黑名单菜单')

    def open_xForce配置_灰色域名劫持_域黑名单(self):
        self.click_iframe(self.loc_xForce配置_灰色域名劫持_域黑名单, self.loc_iframe,
                          '进入xForce配置__灰色域名劫持_域黑名单菜单')

    def open_xProxy配置(self):
        self.click(self.loc_xProxy配置, '进入xProxy配置菜单')

    def open_xProxy配置_基本配置(self):
        self.click_iframe(self.loc_xProxy配置_基本配置, self.loc_iframe,
                          '进入xProxy配置_基本配置菜单')

    def open_xProxy配置_源IP段配置(self):
        self.click_iframe(self.loc_xProxy配置_源IP段配置, self.loc_iframe,
                          '进入xProxy配置_源IP段配置菜单')

    def open_xProxy配置_服务器组配置(self):
        self.click(self.loc_xProxy配置_服务器组配置, '进入xProxy配置_服务器组配置菜单')

    def open_xProxy配置_策略配置(self):
        self.click(self.loc_xProxy配置_策略配置, '进入xProxy配置_策略配置菜单')

    def open_xProxy配置_IP段黑名单(self):
        self.click(self.loc_xProxy配置_IP段黑名单, '进入xProxy配置_IP段黑名单菜单')

    def open_xProxy配置_域黑名单(self):
        self.click(self.loc_xProxy配置_域黑名单, '进入xProxy配置_域黑名单菜单')

    def open_SmartEcho配置(self):
        self.click(self.loc_SmartEcho配置, '进入SmartEcho配置菜单')

    def open_SmartEcho配置_基本配置(self):
        self.click_iframe(self.loc_SmartEcho配置_基本配置, self.loc_iframe,
                          '进入SmartEcho配置_基本配置菜单')

    def open_SmartEcho配置_解析结果黑名单策略(self):
        self.click_iframe(self.loc_SmartEcho配置_解析结果黑名单策略, self.loc_iframe,
                          '进入SmartEcho配置_解析结果黑名单菜单')

    def open_SmartEcho配置_智能解析(self):
        self.click(self.loc_SmartEcho配置_智能解析, '进入SmartEcho配置_智能解析菜单')

    def open_SmartEcho配置_NXR配置(self):
        self.click(self.loc_SmartEcho配置_NXR配置, '进入SmartEcho配置_NXR配置菜单')

    def open_SmartEcho配置_智能解析_源IP段配置(self):
        self.click_iframe(self.loc_SmartEcho配置_智能解析_源IP段配置, self.loc_iframe,
                          '进入SmartEcho配置_智能解析_源IP段配置菜单')

    def open_SmartEcho配置_智能解析_源IP段黑名单配置(self):
        self.click_iframe(self.loc_SmartEcho配置_智能解析_源IP段黑名单配置, self.loc_iframe,
                          '进入SmartEcho配置_智能解析_源IP段黑名单配置菜单')

    def open_SmartEcho配置_智能解析_解析IP段配置(self):
        self.click_iframe(self.loc_SmartEcho配置_智能解析_解析IP段配置, self.loc_iframe,
                          '进入SmartEcho配置_智能解析_解析IP段配置')

    def open_SmartEcho配置_智能解析_智能解析策略配置(self):
        self.click_iframe(self.loc_SmartEcho配置_智能解析_智能解析策略配置, self.loc_iframe,
                          '进入SmartEcho配置_智能解析_智能解析策略配置菜单')

    def open_SmartEcho配置_智能解析_域黑名单配置(self):
        self.click_iframe(self.loc_SmartEcho配置_智能解析_域黑名单配置, self.loc_iframe,
                          '进入SmartEcho配置_智能解析_域黑名单配置菜单')

    def open_SmartEcho配置_NXR配置_重定向IP配置(self):
        self.click_iframe(self.loc_SmartEcho配置_NXR配置_重定向IP配置, self.loc_iframe,
                          '进入SmartEcho配置_NXR配置_重定向IP配置菜单')

    def open_SmartEcho配置_NXR配置_IP段黑名单(self):
        self.click_iframe(self.loc_SmartEcho配置_NXR配置_IP段黑名单, self.loc_iframe,
                          '进入SmartEcho配置_NXR配置_IP段黑名单菜单')

    def open_SmartEcho配置_NXR配置_域黑名单(self):
        self.click_iframe(self.loc_SmartEcho配置_NXR配置_域黑名单, self.loc_iframe,
                          '进入SmartEcho配置_NXR配置_NXR策略配置菜单')

    def login(self, user):
        self.send_keys(self.loc_用户名, user, msg='用户名输入框')
        self.send_keys(self.loc_密码, '123456', msg='密码输入框')
        self.send_keys(self.loc_验证码, '123456', msg='验证码输入框')
        self.submit(self.loc_提交)

    @staticmethod
    def init_net(dnsys1,
                 user1,
                 u10_dev1,
                 dnsys_num=1,
                 sender_num=1,
                 protocol=PROTOCOL):
        """
        :param dnsys1: dnsys 设备对象
        :param user1: user client 设备对象 主要用于拨测
        :param u10_dev1: u10_dev1 用于获得转发服务器
        :param dnsys_num: 初始化dnsys lo网口数量 默认值 1
        :param sender_num: 初始化sender lo网口数量 默认值 1
        :param protocol: ipv4 or ipv6
        :return:
            ipv4:
                dnsys_list [dnsys1_lo_ip, dnsys1_vlan_24, dnsys1_vlan_32],
                sender_list [client1_lo_ip, client1_vlan_24, client1_vlan_32],
                forward_server_ip [1:10]
            ipv6:
                dnsys_list [dnsys1_lo_ip, dnsys1_vlan_112, dnsys1_vlan_128],
                sender_list [client1_lo_ip, client1_vlan_112, client1_vlan_128],
                forward_server_ip [1:10]
        """
        dnsys_list, sender_list = [], []
        if protocol == "ipv4":
            ip_type, subnet1, subnet2, is_ipv4 = 0, 24, 32, True
        else:
            ip_type, subnet1, subnet2, is_ipv4 = 1, 112, 128, False
        # forward_server
        forward_server_ip_list = [
            u10_dev1[1]['forwards'][f'server{i}'][ip_type]
            for i in range(1, 11)
        ]
        # dnsysA
        dnsys1_lo_ip = dnsys1[1]['lo_ips'][ip_type]
        dnsys1_vlan_1 = generate_ip(dnsys1_lo_ip,
                                    subnet1,
                                    is_ipv4=is_ipv4,
                                    is_add_subnet=True)
        dnsys1_vlan_2 = generate_ip(dnsys1_lo_ip,
                                    subnet2,
                                    is_ipv4=is_ipv4,
                                    is_add_subnet=True)
        dnsys_list.append([dnsys1_lo_ip, dnsys1_vlan_1, dnsys1_vlan_2])
        # dnsysX
        for i in range(2, dnsys_num + 1):
            dnsys2_lo_ip = str(i) + dnsys1_lo_ip[
                1:] if ip_type == 0 else dnsys1_lo_ip.replace('::1', f'::{i}')
            dnsys1[0].add_ip_addr_to_network_card(dnsys2_lo_ip)
            dnsys2_vlan_1 = generate_ip(dnsys2_lo_ip,
                                        subnet1,
                                        is_ipv4=is_ipv4,
                                        is_add_subnet=True)
            dnsys2_vlan_2 = generate_ip(dnsys2_lo_ip,
                                        subnet2,
                                        is_ipv4=is_ipv4,
                                        is_add_subnet=True)
            dnsys_list.append([dnsys2_lo_ip, dnsys2_vlan_1, dnsys2_vlan_2])
        # senderA
        client1_lo_ip = user1[1]['lo_ips'][ip_type]
        client1_vlan_1 = generate_ip(client1_lo_ip,
                                     subnet=subnet1,
                                     is_ipv4=is_ipv4,
                                     is_add_subnet=True)
        client1_vlan_2 = generate_ip(client1_lo_ip,
                                     subnet=subnet2,
                                     is_ipv4=is_ipv4,
                                     is_add_subnet=True)
        sender_list.append([client1_lo_ip, client1_vlan_1, client1_vlan_2])
        # senderX
        for i in range(2, sender_num + 1):
            client2_lo_ip = str(i) + client1_lo_ip[
                1:] if ip_type == 0 else client1_lo_ip.replace(
                    '::1', f'::{i}')
            user1[0].add_ip_addr_to_network_card(client2_lo_ip)
            client2_vlan_1 = generate_ip(client2_lo_ip,
                                         subnet=subnet1,
                                         is_ipv4=is_ipv4,
                                         is_add_subnet=True)
            client2_vlan_2 = generate_ip(client2_lo_ip,
                                         subnet=subnet2,
                                         is_ipv4=is_ipv4,
                                         is_add_subnet=True)
            sender_list.append([client2_lo_ip, client2_vlan_1, client2_vlan_2])
        return dnsys_list, sender_list, forward_server_ip_list


def generate_ip(ip: str,
                subnet: int,
                is_ipv4=True,
                is_add_subnet=True,
                is_short_ipv6=True):
    """

    :param ip: ip地址
    :param subnet: 掩码
    :param is_ipv4: 默认传入的地址是iPv4地址
    :param is_add_subnet: 默认返回生成的地址+掩码格式
    :param is_short_ipv6: 默认返回压缩后的ipv6地址

    case1:
        input: generate_ip(ip='192.168.173.130', subnet=23, is_ipv4=True, is_add_subnet=True)
        output: '192.168.172.0/23'  # 地址范围： 192.168.172.0 ~ 192.168.173.255

    case2:
        input: generate_ip(ip='192.168.173.130', subnet=24, is_ipv4=True, is_add_subnet=False)
        output: '192.168.173.0'     # 地址范围： 192.168.172.0 ~ 192.168.173.255

    case3:
        input: generate_ip(ip='fec0:ab34:4334:21ca:901a:1381:c4ab:2625', subnet=64,
                            is_ipv4=False, is_add_subnet=True, is_short_ipv6 = False)
        output: 'fec0:ab34:4334:21ca:0000:0000:0000:0000/64'

    case4:
        input: generate_ip(ip='fec0::21ca:901a:1381:c4ab:2625', subnet=80,
                            is_ipv4=False, is_add_subnet=False, is_short_ipv6 = False)
        output: 'fec0:0000:0000:21ca:901a:0000:0000:0000'

    case5:
        input: generate_ip(ip='fec0::21ca:901a:1381:c4ab:2625', subnet=80,
                            is_ipv4=False, is_add_subnet=False, is_short_ipv6 = True)
        output: 'fec0:0:0:21ca:901a::'

    """

    if is_ipv4:
        if subnet < 1 or subnet > 32:
            raise ValueError("输入IPV4地址掩码不在1~32区间的整数，请检查后重试！")
        s = ''
        for i in ip.split('.'):
            a = bin(int(i))[2:]  # ipv4 10进制字符串转换成2进制字符串
            s += '0' * (8 - len(a)) + a
        # 掩码后面的数字反转 0->1 1->0
        p = s[:subnet] + "0" * (32 - subnet)
        gen_ip_address = ".".join(
            [str(int(p[j * 8:(j + 1) * 8], 2)) for j in range(4)])
    else:
        if subnet < 1 or subnet > 128:
            raise ValueError("输入IPV6地址掩码不在1~128区间的整数，请检查后重试！")
        if "::" in ip:
            s1, s2 = "", ""
            p1 = ip.split("::")[0]
            p2 = ip.split("::")[1]
            for i in p1.split(":"):
                a = bin(int(i, 16))[2:]
                s1 += '0' * (16 - len(a)) + a
            for i in p2.split(":"):
                a = bin(int(i, 16))[2:]
                s2 += '0' * (16 - len(a)) + a
            s = s1 + '0' * (128 - len(s1) - len(s2)) + s2
        else:
            s = ""
            for i in ip.split(":"):
                a = bin(int(i, 16))[2:]
                s += '0' * (16 - len(a)) + a
        p = s[:subnet] + "0" * (128 - subnet)
        gen_ip_address = ":".join([
            hex(int(p[j * 16:(j + 1) * 16], 2))[2:].zfill(4) for j in range(8)
        ])
        gen_ip_address = ipaddress.IPv6Address(
            gen_ip_address) if is_short_ipv6 else gen_ip_address

    if is_add_subnet:
        return str(gen_ip_address) + "/" + str(subnet)
    else:
        return str(gen_ip_address)
