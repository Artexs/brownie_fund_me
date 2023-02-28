from brownie import FundMe, MockV3Aggregator, network, config
import time
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print("TEST1")
    # txn = fund_me.withdraw()
    # print("TEST2")
    # txn.wait(1)
    print(f"Contract deployed to {fund_me.address}")
    # txn.wait(2)
    time.sleep(1)
    return fund_me


def main():
    deploy_fund_me()
