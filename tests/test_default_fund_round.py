from config.envs.default import DefaultConfig
from fsd_utils.config.commonconfig import CommonConfig

def test_default_fund_id():
    assert CommonConfig.COF_FUND_ID == DefaultConfig.DEFAULT_FUND_ID

def test_default_round_id():
    assert CommonConfig.COF_ROUND_2_W3_ID == DefaultConfig.DEFAULT_ROUND_ID