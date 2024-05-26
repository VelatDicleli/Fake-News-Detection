import React, { useState } from 'react';
import axios from 'axios';
import { FaThumbsUp, FaThumbsDown } from 'react-icons/fa';

const PredictionForm = () => {
  const [formData, setFormData] = useState({
    title: '',
    text: ''
  });
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); 
    if (!formData.title || !formData.text) {
      setError('Please fill in both fields.');
      return;
    }
    try {
      const response = await axios.post('http://127.0.0.1:8000/predict', formData);
      setPrediction(response.data.predicted_class);
    } catch (error) {
      setError('An error occurred while processing your request');
      console.error('Error:', error);
    }
  };

  return (
    <div className="container py-5">
      <h2 className="text-center mb-4">Question Whether The News Is Fake Or Not</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="title" className="form-label">Title:</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            className="form-control"
            style={{ width: '1000px' }}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="text" className="form-label">Text:</label>
          <textarea
            id="text"
            name="text"
            value={formData.text}
            onChange={handleChange}
            className="form-control"
            style={{ width: '1000px', height: '250px' }}
          />
        </div>
        <button type="submit" className="btn btn-success">Submit</button>
      </form>
      {error && <div className="alert alert-warning mt-4">{error}</div>}
      {prediction !== null && !error && (
        <div className="mt-4">
          <h3 className="text-center" style={{ color: 'white' }}>Result:</h3>
          <h1 className="text-center" style={{ color: prediction == 1 ? '#09FF00' : '#bf0000' }}>
            {prediction == 1 ? 'It is real' : 'It is fake'} {prediction == 1 ? (
              <FaThumbsUp style={{ fontSize: '40px', color: '#0ad10a' }} />
            ) : (
              <FaThumbsDown style={{ fontSize: '40px', color: 'red' }} />
              
            )}
          </h1>
        </div>
      )}
    </div>
  );
};

export default PredictionForm;
