//SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Storage {
    struct FileInfo {
        string hash;
    }

    FileInfo[] public files;

    function addFile(string memory _hash) public {
        FileInfo memory newFile = FileInfo(_hash);
        files.push(newFile);
    }

    function getFiles() public view returns (FileInfo[] memory) {
        return files;
    }
}
