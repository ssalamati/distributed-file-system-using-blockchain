import React, { useEffect, useState } from 'react';
import axios from 'axios';
import FormData from 'form-data';
import Web3 from 'web3';

import { NETWORK_ID, NETWORK_URL, STORJ_IPFS_API_URL, STORJ_IPFS_GATEWAY_URL } from './constants';
import FilesTable from './components/FilesTable/FilesTable'
import StorageContract from './artifacts/contracts/Storage.json'
import './App.css';


function App() {
	const [selectedFile, setSelectedFile] = useState(null);
	const [uploadedFiles, setUploadedFiles] = useState([]);
	const [contract, setContract] = useState([]);
	const [account, setAccount] = useState([]);

	useEffect(() => {
		const init = async () => {
		  const web3 = new Web3(NETWORK_URL);
		  const contract = new web3.eth.Contract(StorageContract.abi, StorageContract.networks[NETWORK_ID].address);
		  setContract(contract);

		  const accounts = await web3.eth.getAccounts();
		  setAccount(accounts[0]);

		  const uploadedFiles = await contract.methods.getFiles().call();
		  setUploadedFiles(uploadedFiles);
		}
		init();
	  }, []);

	const handleFileChange = (event) => {
		setSelectedFile(event.target.files[0]);
	};

	const handleSubmit = async (event) => {
		event.preventDefault();

		let data = new FormData();
		data.append('file', selectedFile);

		try {
			const response = await axios.post(STORJ_IPFS_API_URL, data, {
				headers: {
					'Content-Type': `multipart/form-data; boundary= ${data._boundary}`,
				},
				maxContentLength: Infinity,
				maxBodyLength: Infinity,
			});

			await contract.methods.addFile(response.data).send({from: account, gas: '1000000'});

			window.location.reload(false);
		} catch (error) {
			console.error(error);
		}
	}

	return (
		<div className="App">
		<header className="App-header">
			<FilesTable files={uploadedFiles.map(fileHash => ({url: `${STORJ_IPFS_GATEWAY_URL}${fileHash}`, name: fileHash, size: ""}))}/>
			<h5>
			Upload a file
			</h5>
			<form onSubmit={handleSubmit}>
				<input type="file" onChange={handleFileChange}/>
				<input type="submit"/>
			</form>
		</header>
		</div>
	);
}

export default App;
