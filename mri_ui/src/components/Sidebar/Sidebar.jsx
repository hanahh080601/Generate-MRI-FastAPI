import React from "react";
import { Link } from 'react-router-dom'
import {
    faLaptop,
    faArrowUpFromBracket
} from "@fortawesome/free-solid-svg-icons";
import {faKeyboard} from "@fortawesome/free-regular-svg-icons"

import "./sidebar.css"
import SidebarItem from "./SidebarItem";

function Sidebar() {
    return <div className="sidebar">
        <div className="logo-container">
            <img className="logo-image" src="/brain_illus-removebg.png" alt="brain_logo"/>
            <div className="logo-name">
                <Link to="/" className="logo__s1">HANA</Link>
                <Link to="/" className="logo__s2">MRI</Link>
            </div>
        </div>
        <div className="sidebar-content">
            <SidebarItem icon={faArrowUpFromBracket} label={"Upload file"} to="/upload_page" />
            <SidebarItem icon={faKeyboard} label={"Input contrast"} to="/input_page" />
            <SidebarItem icon={faLaptop} label={"Choose model"} to="/choose_model" />
        </div>
        <div className="sidebar-footer"></div>
    </div>
}

export default Sidebar;