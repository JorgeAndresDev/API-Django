const GetAllSuppliers = async () => {
  const { data } = await axios.get("/resources/suppliers/get_all_suppliers");
  return data;
};
