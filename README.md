# Distributed File System Using Blockchain
##  Overview
This project is a decentralized file storage system built on the blockchain. It allows users to upload and manage files in a decentralized and secure manner using the Ethereum blockchain. The project is divided into three main components: the blockchain smart contracts, the React client, and the Python server.

![gif](demo.gif?raw=true "gif")

## Prerequisites
Before running this project, make sure you have the following software installed:

Truffle: A development framework for Ethereum smart contracts.\
Node.js: A JavaScript runtime environment.\
Ganache: A personal Ethereum blockchain for local development.
## Setup
### 1. Run Ganache
Start Ganache with the following configurations:

Network ID: 5777\
RPC Server: http://127.0.0.1:7545
### 2. Compile and Migrate Smart Contracts
Navigate to the "blockchain" folder and run the following commands:

### `truffle compile`
### `truffle migrate`
This will compile and deploy the smart contracts to the local Ganache blockchain. After migration, copy the "Storage.json" file from "blockchain/build/contracts" to "client/src/artifacts/" and replace the existing "Storage.json" file.

### 3. Install Dependencies for React Client
Navigate to the "client" folder and run the following command:

### `npm install`
This will install the required dependencies for the React client.

### 4. Run React Client
In the "client" folder, run the following command to start the React client on "http://localhost:3000/":

### `npm run start`
### 5. Setup Python Server

Navigate to the "server" folder and create a virtual environment with the following command:
### `python3 -m venv venv`
Activate the virtual environment with the following command:
### `source venv/bin/activate`
Install the dependencies for the Python server with the following command:
### `pip3 install -r requirements.txt`
### 6. Run Python Server
In the "server" folder, run the following command to start the Python server:

### `python3 run server`
### 7. Upload Files
Now you can access the React client in your web browser at "http://localhost:3000/" and use it to upload and manage files in the decentralized file storage system.

## Additional Notes
If you need to have more nodes for testing, you can use Vagrant to set up additional virtual machines with Ganache instances.
## License
This project is licensed under the MIT License.