from pathlib import Path

class Config:
    """应用程序配置管理类"""
    
    # 项目根目录
    BASE_DIR = Path(__file__).parent
    
    # 数据目录
    DATA_DIR = BASE_DIR / "Data"
    
    # UI目录
    UI_DIR = BASE_DIR / "UI"
    
    # 日志配置
    LOG_FILE = DATA_DIR / "Paissa.log"
    HISTORY_FILE = DATA_DIR / "Paissa_query_history.log"
    ITEM_DATA_FILE = DATA_DIR / "item.Pdt"
    MARKETABLE_FILE = DATA_DIR / "marketable.py"
    VERSION_FILE = DATA_DIR / "version"
    
    # API配置 - 针对国内访问优化
    API_HEADERS = {
        "User-Agent": "Paissa/1.0",
        "referer": "http://Paissa.public/",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate"
    }
    
    # 网络超时设置 - 短而快
    TIMEOUT_SETTINGS = {
        "version_check": 3,       # 版本检查3秒超时
        "data_download": 5,       # 数据下载5秒超时  
        "market_data": 3,         # 市场数据6秒超时
        "icon_download": 3        # 图标下载3秒超时
    }
    
    # 并发设置 - 多重试
    MAX_WORKERS = 20
    MAX_RETRY_ATTEMPTS = 3        # 增加重试次数到3次
    RETRY_DELAY_BASE = 0.5        # 基础重试延迟0.5秒
    
    # 缓存设置
    PRICE_CACHE_SIZE = 1000
    CACHE_EXPIRE_TIME = 300  # 5分钟

    # 服务器配置
    SERVER_CONFIG = {
        "version": "1.0",
        "world_regions": {
            "maoxiaopang": ["猫小胖", "紫水栈桥", "延夏", "静语庄园", "摩杜纳", "海猫茶屋", "柔风海湾", "琥珀原"],
            "luxingniao": ["陆行鸟", "红玉海", "神意之地", "拉诺西亚", "幻影群岛", "萌芽池", "宇宙和音", "沃仙曦染", "晨曦王座"],
            "moguli": ["莫古力", "白银乡", "白金幻象", "神拳痕", "潮风亭", "旅人栈桥", "拂晓之间", "龙巢神殿", "梦羽宝境"],
            "doudouchai": ["豆豆柴", "水晶塔", "银泪湖", "太阳海岸", "伊修加德", "红茶川"],
            "Elemental": ["Elemental", "Carbuncle", "Kujata", "Typhon", "Garuda", "Atomos", "Tonberry", "Aegis", "Gungnir"],
            "Gaia": ["Gaia", "Alexander", "Fenrir", "Ultima", "Ifrit", "Bahamut", "Tiamat", "Durandal", "Ridill"],
            "Mana": ["Mana", "Asura", "Pandaemonium", "Anima", "Hades", "Ixion", "Titan", "Chocobo", "Masamune"],
            "Aether": ["Aether", "Jenova", "Faerie", "Siren", "Gilgamesh", "Midgardsormr", "Adamantoise", "Cactuar", "Sargatanas"],
            "Primal": ["Primal", "Famfrit", "Exodus", "Lamia", "Leviathan", "Ultros", "Behemoth", "Excalibur", "Hyperion"],
            "Chaos": ["Chaos", "Omega", "Moogle", "Cerberus", "Louisoix", "Spriggan", "Ragnarok", "Sagittarius", "Phantom"],
            "Light": ["Light", "Twintania", "Lich", "Zodiark", "Phoenix", "Odin", "Shiva", "Alpha", "Raiden"],
            "Crystal": ["Crystal", "Brynhildr", "Mateus", "Zalera", "Diabolos", "Coeurl", "Malboro", "Goblin", "Balmung"],
            "Materia": ["Materia", "Ravana", "Bismarck", "Sephirot", "Sophia", "Zurvan"],
            "Meteor": ["Meteor", "Belias", "Shinryu", "Unicorn", "Yojimbo", "Zeromus", "Valefor", "Ramuh", "Mandragora"],
            "Dynamis": ["Dynamis", "Marilith", "Seraph", "Halicarnassus", "Maduin"]
        },
        "area_mappings": {
            "China": ["maoxiaopang", "moguli", "luxingniao", "doudouchai"],
            "Japan": ["Elemental", "Gaia", "Mana", "Meteor"],
            "North-America": ["Aether", "Primal", "Crystal", "Dynamis"],
            "Oceania": ["Materia"],
            "Europe": ["Chaos", "Light"]
        }
    }

    # 界面资源
    HQ_ICON_FILE = DATA_DIR / "hq.png"
    PROGRAM_VERSION = "2.1.0"

    # API基础URL
    UNIVERSALIS_BASE_URL = "https://universalis.app"
    GARLANDTOOLS_BASE_URL = "https://garlandtools.cn"
    CAFEMAKER_BASE_URL = "https://cafemaker.wakingsands.com"
    OSS_DATA_BASE_URL = "https://paissa-data.oss-cn-hongkong.aliyuncs.com"
    GITEE_RAW_BASE_URL = "https://gitee.com/nagaresst/paissa/raw/master"
    
    @classmethod
    def get_data_path(cls, filename):
        """获取数据文件完整路径"""
        return cls.DATA_DIR / filename
    
    @classmethod
    def get_ui_path(cls, filename):
        """获取UI文件完整路径"""
        return cls.UI_DIR / filename