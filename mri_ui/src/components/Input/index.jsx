import "./styles.sass";

export default function Input({ value, setValue, name, placeholder }) {
    return (
        <div className="form__group field">
            <input
                className="form__field"
                type="text"
                name={name}
                onChange={(e) => {
                    setValue(e.target.value);
                }}
                placeholder={placeholder}
                value={value}
            />
            <label className="form__label">{placeholder}</label>
        </div>
        
    );
}
