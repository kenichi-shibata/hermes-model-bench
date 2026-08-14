function handleSubmit(e) {
  api.post('/submit', formData);
  // missing e.preventDefault()
}
