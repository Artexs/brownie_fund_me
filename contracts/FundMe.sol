// SPDX-License-Identifier: MIT

pragma solidity >=0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    AggregatorV3Interface public priceFeed;
    address owner;
    address[] public founders;

    constructor(address _priceFeed) {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    mapping(address => uint256) public UserFunds;

    function getLatestPriceWEIUSD() public view returns (uint256) {
        (, int256 price, , , ) = priceFeed.latestRoundData();
        return uint256(price * 10000000000);
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    function getConversionRate(uint256 ethAmount)
        internal
        view
        returns (uint256)
    {
        uint256 latestPrice = getLatestPriceWEIUSD();
        return (ethAmount * latestPrice) / 10**18;
    }

    function fund() public payable returns (uint256) {
        require(
            getConversionRate(msg.value) >= 20 * 10**18,
            "You need to pay at least 20 USD"
        );
        UserFunds[msg.sender] += msg.value;
        founders.push(msg.sender);
        return msg.value;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "You are not an Owner");
        _;
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
        for (uint256 index = 0; index < founders.length; index++)
            UserFunds[founders[index]] = 0;
        founders = new address[](0);
    }
}
