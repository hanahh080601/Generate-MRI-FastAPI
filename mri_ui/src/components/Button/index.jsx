import "./button.css"

export default function Button({ children, onClick }) {
    return (
        <button className="input-form-button" onClick={onClick}>
            {children}
        </button>
    )
}