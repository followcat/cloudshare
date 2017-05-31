# -*- coding: utf-8 -*-


added_words = {
    # IBA - 现场服务工程师:
    'e3bd422a2d6411e6b5296c3be51cefca': u'电气 自动化 工程机械 PLC 程序 发电机 平台 调试 设备 工控机、触摸屏 控制系统 电气设备 西门子 施耐德 三菱',
    # IBA - Flying Engineer- Beam Physics 亚太区服务工程师--束流物理方向:
    '4f2d032e53e911e685e24ccc6a30cd76': u'Matlab Ansys 蒙特卡洛 束流 超导 磁体 电磁场 真空 磁共振 耦合 物理 高能 原子核物理 粒子物理 加速器 磁铁 低温 医疗',
    # IBA - 现场服务工程师 (淄博万杰质子中心）:
    '86119050313711e69b804ccc6a30cd76': u'电气 电子 电路 加速器 质子 放射 安装 维护 调试 维修 技术支持 PACS',
    # IBA - Application Specialist/Medical Physicist 亚太区服务工程师--应用专员/医学物理师:
    '9b48f97653e811e6af534ccc6a30cd76': u'医学 物理师 研究员 放射 放疗 医学物理 CT MRI 磁共振',
    # IBA - Flying Engineer - Cyclotron 亚太地区服务工程师--加速器方向:
    'e9f415f653e811e6945a4ccc6a30cd76': u'电气 加速器 射频 谐振 质子 直线 回旋 核仪器 核辐射 安装 维护 调试',
    # HHMT - 应用软件工程师:
    '48dc231c0b5d11e6b89e6c3be51cefca': u'数据库 PACS RIS DICOM 图像 界面 通信协议 模块 测试 优化 算法 数据 流程图 下位机 客户端 服务端 医院',
    # HHMT - 系统软件工程师:
    'def2a4120b5c11e691246c3be51cefca': u'EPICS Qt labVIEW 协议 通信 数据 测试 治疗 控制 系统 串口 上位机 下位机 设计 通信 编程 DICOM sql 数据库 OPC',
    # HHMT - 高级应用软件工程师:
    '06fdc0680b5d11e6ae596c3be51cefca': u'PACS RIS DICOM 图像 QT HL7 通信协议 客户 需求 测试 开发 算法 接口 数据结构 设计 编程 管理',
    # HHMT - 高级电气工程师:
    'be97722a0cff11e6a3e16c3be51cefca': u'电气 PLC FPGA 设备 电气设备 ABB EMC IEC 架构 设计 CT X 数据 方案 接口 可靠性 控制 GE 东芝 电路板 协议 标准 系统设计',
    # HHMT - 加速器物理部负责人（ Accelerator Physics Department Head）:
    'a9a20a84473211e6a6934ccc6a30cd76': u'',
    # HHMT - 高级风险管理工程师:
    'fb2ac1c80b4d11e6adce6c3be51cefca': u'医疗 设备 调研 选型 风险 缺陷 故障 跟踪 可靠性 验证 政策 标准 法规',
    # HHMT - 项目经理:
    '048b4bc60d0011e6be436c3be51cefca': u'协调 研发 计划 监控 超声系统 MRI CT 设计 评测 项目管理 产品设计 系统开发 产品化 DFMEA 英文 GE 西门子',
    # HHMT - 高级系统测试工程师:
    '684605740b4e11e6ba746c3be51cefca': u'',
    # HHMT - 现场过程工艺及文档控制工程师:
    '8c43b5343c4511e680994ccc6a30cd76': u'安装 施工 工艺 过程 流程 配置 调试 指导书 检验 标准 沟通 整机 模块 整理 手册 文档 资料 编写',
    # HHMT - 项目主管:
    '7858d9aa636411e6815f4ccc6a30cd76': u'',
    # 费森尤斯卡比健源 - PC software engineer:
    '07ea1a8018be11e684026c3be51cefca': u'上位机 下位机 编程 数据库 SQL windows WPF 控件 接口 UI 界面 PC vs visual studio NET 客户端 服务端',
    # 费森尤斯卡比健源 - Project manager:
    '2fe1c53a231b11e6b7096c3be51cefca': u'进度 交付 协议 注射泵 仪器 营养泵 输液泵',
    # 费森尤斯卡比健源 - 全球产品经理--Global product manager:
    'ae31247274c811e6b6b54ccc6a30cd76': u'',
    # 费森尤斯卡比健源 - 生产线验证 工程师:
    'd33a669c313511e69edc4ccc6a30cd76': u'检验 验证 ISO FDA qsr 质量 工艺 VALIDATION 流程 改进 装配 医疗 审核 工艺设计 工艺方案 工艺策划',
    # IBA - EHS/RSO Manager APAC 亚太区核安全经理:
    'e290dd36428a11e6b2934ccc6a30cd76': u'',
    # 安健科技 - (Null):
    '763199560a9411e6a7936c3be51cefca': u'医疗 图像 超声 HIS PACS 影像 DICOM 仪器 报告 医疗软件 超声 诊断',
    # HHMT - 高级嵌入式软件工程师:
    '437958560b5b11e6aaa86c3be51cefca': u'医疗 DSP ARM 医疗设备 监护仪 心电 血氧 超声 影像 CT MRI 上位机 下位机 体温',
    # 费森尤斯卡比健源 - 硬件工程师:
    '80ce049a320711e6ac1f4ccc6a30cd76': u'PCB EMC 医用 超声',
    # 费森尤斯卡比健源 - 机械/结构工程师:
    'cce2a5be547311e6964f4ccc6a30cd76': u'医疗设备 CAD 工艺 生产 制作 安装 调试 电机 结构 机械 设计',
    #HHMT    市场销售部经理:
    '672ec6ce849511e6a6af4ccc6a30cd76': u'市场 销售 销售部 销售额 营销 产品 渠道 大区 经理 主管 计划 拓展 客户 展销 代理商 调研',
    #HHMT   市场专员--市场销售部
    '97fe1b086f2111e69f834ccc6a30cd76': u'市场 销售 销售代表 销售部 销售额 营销 产品 渠道 专员 计划 拓展 客户 展销 代理商 调研',
}
