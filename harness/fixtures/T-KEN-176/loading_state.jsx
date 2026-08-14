function useData() {
  const [loading, setLoading] = useState(false);
  const fetch = async () => {
    setLoading(true);
    try { const d = await api.get(); setData(d); }
    catch (e) { setLoading(false); }
  };
}
