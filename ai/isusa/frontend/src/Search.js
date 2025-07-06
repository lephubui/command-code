import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function Search({ email }) {
    const [stage, setStage] = useState('College/University Academy'); // Set default stage
    const [question, setQuestion] = useState('');
    const [advice, setAdvice] = useState('');
    const navigate = useNavigate(); // Import and use the useNavigate hook

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await axios.post('http://localhost:5001/api/advice', { email, stage, question });
        setAdvice(response.data.advice);
    };

    const handleCreatePlan = () => {
        navigate('/create-plan', { state: { advice } }); // Pass advice as state
    };

    return (
        <div className="container mt-5">
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h1>International Student USA Journey</h1>
            </div>
            <form onSubmit={handleSubmit} className="mb-4">
                <div className="form-group">
                    <label htmlFor="stage">Stage:</label>
                    <select
                        id="stage"
                        className="form-control"
                        value={stage}
                        onChange={(e) => setStage(e.target.value)}
                    >
                        <option value="College/University Academy">College/University Academy</option>
                        <option value="Internship Hunting">Internship Hunting</option>
                        <option value="Post-Graduation and Career Growth">Post-Graduation and Career Growth</option>
                        <option value="Seeking H1b, EB3, and EB2">Seeking H1b, EB3, and EB2</option>
                        <option value="Life After Green Card">Life After Green Card</option>
                    </select>
                </div>
                <div className="form-group">
                    <label htmlFor="question">Question:</label>
                    <input
                        type="text"
                        id="question"
                        className="form-control"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                    />
                </div>
                <button type="submit" className="btn btn-primary">Get Advice</button>
            </form>
            {advice && (
                <div className="card">
                    <div className="card-body">
                        <h2 className="card-title">Advice:</h2>
                        <p className="card-text">{advice}</p>
                    </div>
                </div>
            )}
            <button className="btn btn-secondary mt-4" onClick={() => navigate('/history')}>View History</button>
            {advice && (
                <button className="btn btn-success mt-4" onClick={handleCreatePlan}>Create a Plan</button>
            )}
        </div>
    );
}

export default Search;