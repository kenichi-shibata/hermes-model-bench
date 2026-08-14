function MyButton() {
  const handleClick = () => console.log('clicked');
  return <button>Click me</button>; // handleClick never attached
}
