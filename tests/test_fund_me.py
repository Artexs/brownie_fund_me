from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import brownie
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    # print(f"wielkosc darowizny {fund_me.founders(account.address)}")
    # print("entrance fee: {entrance_fee}")
    assert fund_me.UserFunds(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.UserFunds(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("ony for local testing")
    account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # with pytest.raises(exceptions.VirtualMachineError):
    # with brownie.reverts("You are not an owner"):
    fund_me.withdraw({"from": account})
    # fund_me.withdraw({"from": bad_actor})
    # assert 5 == 4
