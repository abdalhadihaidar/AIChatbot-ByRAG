import React, { useState } from 'react';
import './App.css';
import TextInputForm from './components/TextInputForm';
import FilesInputForm from './components/FilesInputForm';
import QAInputForm from './components/QAInputForm';
import WebsiteInputForm from './components/WebsiteInputForm';
import FloatingButton from './components/FloatingButton'; // Import the Floating Button
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
    const [activeTab, setActiveTab] = useState('text');

    return (
        <div className="App">
            <h1>Input Submission Portal</h1>
            <div className="tab-bar">
                <button onClick={() => setActiveTab('text')} className={activeTab === 'text' ? 'active' : ''}>
                    Text
                </button>
                <button onClick={() => setActiveTab('files')} className={activeTab === 'files' ? 'active' : ''}>
                    Files (PDF, CSV, Text)
                </button>
                <button onClick={() => setActiveTab('qa')} className={activeTab === 'qa' ? 'active' : ''}>
                    Q&A
                </button>
                <button onClick={() => setActiveTab('website')} className={activeTab === 'website' ? 'active' : ''}>
                    Websites
                </button>
            </div>

            {/* Conditional rendering based on active tab */}
            {activeTab === 'text' && <TextInputForm />}
            {activeTab === 'files' && <FilesInputForm />}
            {activeTab === 'qa' && <QAInputForm />}
            {activeTab === 'website' && <WebsiteInputForm />}

            {/* Add the floating button for the chatbot */}
            <FloatingButton />

            {/* Toast container to show notifications */}
            <ToastContainer />
        </div>
    );
}

export default App;
