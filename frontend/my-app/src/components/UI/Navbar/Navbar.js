import React,{useState} from "react"
import "../../../styles.scss"
// import module_css from './Navbar.module.css'




export default function Navbar(){

   

    return (
      
      <div className="topnav" id="myTopnav">
      <a href="#home" className="active">Home</a>
      <a href="#Browse">Browse</a>
      <a href="#Request">Request</a>
      <a href="#about">About</a>
      <div className="dropdown">
        <button className="dropbtn">Dropdown
          <i className="fa fa-caret-down"></i>
        </button>
        <div className="dropdown-content">
          <a href="#">Link 1</a>
          <a href="#">Link 2</a>
          <a href="#">Link 3</a>
        </div>
      </div>
      <a href="javascript:void(0);" className="icon" ></a>
    </div>
    )    
    }