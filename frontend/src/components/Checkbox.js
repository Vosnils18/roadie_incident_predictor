import React from "react";

const Checkbox = ({ label, onChange, checked }) => {
  return (
    <label className="checkbox text-cyan-900 underline py-2 flex items-center gap-2">
      <input
        type="checkbox"
        name={label}
        checked={checked}
        onChange={onChange}
      />
      {label}
    </label>
  );
};

export default Checkbox;