import React from 'react';

interface InputFieldProps {
  type: string;
  label: string;
  name: string;
  placeholder: string;
  value: string | number;
  options?: string[]; // Only for select inputs
  onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => void;
  required?: boolean;
}

const InputField: React.FC<InputFieldProps> = ({
  type,
  label,
  name,
  placeholder,
  value,
  options,
  onChange,
  required = false,
}) => {
  return (
    <div>
      <label htmlFor={name} className="block text-gray-700 font-normal text-sm">
        {label}
      </label>
      {type === 'select' ? (
        <select
          name={name}
          id={name}
          value={value}
          onChange={onChange}
          className="mt-2 p-3 py-2 w-full border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder:text-sm"
          required={required}
        >
          <option value="" disabled></option>
          {options?.map((option, index) => (
            <option key={index} value={option}>
              {option}
            </option>
          ))}
        </select>
      ) : (
        <input
          type={type}
          id={name}
          name={name}
          value={value}
          onChange={onChange}
          className="mt-2 p-3 py-2 w-full border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 placeholder:text-sm"
          required={required}
          placeholder={placeholder || ''}
        />
      )}
    </div>
  );
};

export default InputField;
