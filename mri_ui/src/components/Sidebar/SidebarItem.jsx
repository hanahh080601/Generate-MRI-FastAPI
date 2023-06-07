import { Link, useLocation } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import classnames from 'classnames'

import "./sidebar.css";

export default function SidebarItem({ label, icon, to }) {
    const { pathname } = useLocation()
    return (
        <Link className={classnames({ "sidebar-item": true, active: pathname === to })} to={to}>
            <FontAwesomeIcon icon={icon} className="sidebar-item__icon" />
            <span className="sidebar-item__label">{label}</span>
        </Link>
    );
}
