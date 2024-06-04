import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function SearchForm({ handleDataFromSearchForm }) {
    const [submitting, setSubmitting] = useState(false);
    const [vehMakeCacheData, setVehMakeCacheData] = useState([]);
    const navigate = useNavigate();

    const ROOT_API_URLS = [
        "https://64.23.253.75:3443/api",
        "http://localhost:7777/api",
        "http://localhost:3000/api",
        "https://localhost:3443/api",
        "http://64.23.253.75:3443/api",
        "http://64.23.253.75:3000/api"
    ];

    useEffect(() => {
        const loadManufacturerCache = async () => {
            try {
                for (const rootURL of ROOT_API_URLS) {
                    const specificRoute = "retrieve_cache";
                    const fullURL = `${rootURL}/${specificRoute}`;
                    console.log("trying url: ",fullURL)
	            const response = await fetch(fullURL,{
			method:'GET',
			timeout:10000});
                    if (response.ok) {
                        const data = await response.json();
                        setVehMakeCacheData(data);
                        console.log("data: ",data);
                        break; // Stop trying URLs if successful response
                    }
                }
            } catch (error) {
                console.log("Error retrieving cache data from server:", error);
            }
        };
        loadManufacturerCache();
    }, []);

    const handleFormSubmit = async (e) => {
        e.preventDefault();
        console.log("Form submitted");

        // Add form data processing logic here

        try {
            // Add logic to call the server with the form data
        } catch (error) {
            console.error('Error with form submission:', error.message);
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className='search-form-wrapper'>
            <form onSubmit={handleFormSubmit}>
                <label>Enter Your Search here:
                    <input 
                        type='text'
                        name='search_query'
                        placeholder='Search For A vehicle (ex. Toyota Supra or 2003 M5)'
                    />       
                </label>
                <button type='submit'>Submit</button>
            </form>
        </div>
    );
}
