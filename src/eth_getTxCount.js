let Web3 = require('web3');
const web3 = new Web3(new Web3.providers.HttpProvider('https://ropsten.infura.io/v3/33bc94be093043008a20f6b8fc65c576'))

let metamask_account = '0x220a530fBBfE397C9F95279117fEf25e4490dA90'
let contract = '0xd196e1105e638D71Ea0a03f902cCd3342E7bc0c2'
let contract_2 = '0xDA9Dd3bc865bd34aF3c5FAA2E6E16bf78a69CDa8'

web3.eth.getTransactionCount(contract)
.then(nonce=>console.log("CA1:",contract,nonce));

web3.eth.getTransactionCount(contract_2)
.then(nonce=>console.log("CA2:",contract_2,nonce));

web3.eth.getTransactionCount(metamask_account)
.then( nonce=>console.log("EOA:",metamask_account,nonce));