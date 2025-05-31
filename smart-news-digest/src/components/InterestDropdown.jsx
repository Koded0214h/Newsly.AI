import Select from "react-select";

const interestOptions = [
  { value: "Technology", label: "Technology" },
  { value: "Politics", label: "Politics" },
  { value: "Health", label: "Health" },
  { value: "Science", label: "Science" },
  { value: "Business", label: "Business" },
  { value: "Sports", label: "Sports" },
  { value: "Entertainment", label: "Entertainment" },
  { value: "Gaming", label: "Gaming" },
  { value: "Travel", label: "Travel"},
  { value: "Education", label: "Education"},
  { value: "Arts and Culture", label: "Arts and Culture"},
  { value: "Food", label: "Food"},
  { value: "Finanace", label: "Finanace"},
  { value: "History", label: "History"},
  { value: "Books", label: "Books"},
  { value: "Relationship", label: "Relationship"},
  { value: "Lifestyle", label: "Lifestyle"},
  { value: "Startups", label: "Startups"},
  { value: "Environment", label: "Environment"},
  { value: "Music", label: "Music"},
  { value: "Travel", label: "Travel"},
  { value: "AI", label: "AI & Machine Learning" },
];

export default function InterestDropdown({ selected, setSelected }) {
  const handleChange = (selectedOptions) => {
    setSelected(selectedOptions || []);
  };

  return (
    <div className="mb-6">
      <label className="block mb-1 font-semibold text-blue-900 ">Select Your Interests</label>
      <Select
        isMulti
        name="interests"
        options={interestOptions}
        className="basic-multi-select "
        classNamePrefix="select"
        value={selected}
        onChange={handleChange}
      />
    </div>
  );
}
