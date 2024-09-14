import React, { useState } from 'react';
import axios from 'axios';

const FilesInputForm = () => {
    const [files, setFiles] = useState(null);  // Store selected files
    const [responseMessage, setResponseMessage] = useState('');  // Store response message

    // Handle file selection
    const handleFileChange = (e) => {
        setFiles(e.target.files);  // Get the selected files from input
    };

    // Handle form submission (upload)
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!files || files.length === 0) {
            setResponseMessage("No file selected.");
            return;
        }

        const formData = new FormData();  // Create FormData object
        formData.append('file', files[0]);  // Add the file to the form data

        try {
            const response = await axios.post('http://localhost:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',  // Ensure the content type is multipart/form-data
                },
            });
            setResponseMessage(response.data.message || "File uploaded successfully.");
        } catch (error) {
            setResponseMessage("Error: " + (error.response?.data?.error || error.message));
        }
    };

    return (
        <div>
            <h2>Submit Files (PDF, CSV, Text)</h2>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileChange} accept=".pdf,.txt,.csv" />
                <br />
                <button type="submit">Upload</button>
            </form>
            <p>{responseMessage}</p>
        </div>
    );
};

export default FilesInputForm;
