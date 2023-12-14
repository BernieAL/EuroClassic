import React, {useState} from 'react'



export default function SearchForm(){

    // if form submitted and awaiting server response - disable 'submit' button
    const [submitting,setSubmitting] = useState(false)

    
    const [formData,setFormData] = useState({
        year:'',
        make:'',
        model:'',
    })

    const handleFormSubmit = async (e) =>{
        e.preventDefault()
test
        // make call to backend api
        try{
            const response = await fetch('http://127.0.0.1:5000/vehicle-query',{
                method: 'POST',
                headers: {
                    'Content-Type':'application/json',
                },
                body:JSON.stringify(formData)
            })
            if (!response.ok){
                throw new Error ('Problem with response from server')
            } else {
                // render other components to display the data
                console.log('Form submitted successfully',response)
            }
        } catch (error) {
            //handle fetch errors
            console.error('Error with form submission', error.message)
        } finally {
            
            setSubmitting(false);
        }
    }

    const handleFormChange = (e)=>{
        const {name,value} = e.target 
        setFormData((prevData)=>({
            ...prevData,
            [name]: value,
        }))
    }

    return(
        
        <div className='search-form-wrapper'>
            <form onSubmit={handleFormSubmit}>
                <label>YEAR:
                    <input 
                        type='text'
                        name='year'
                        value={formData.year}
                        onChange={handleFormChange} />
                </label>
                <label>MAKE:
                    <input 
                        type='text'
                        name='make'
                        value={formData.make}
                        onChange={handleFormChange} />
                </label>
                <label>MODEL:
                    <input 
                        type='text'
                        name='model'
                        value={formData.model}
                        onChange={handleFormChange} />
                </label>
                <button type='submit'>Submit</button>
            </form>
        </div>
    )
}