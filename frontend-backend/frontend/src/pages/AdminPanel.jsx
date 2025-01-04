import Hero from "../components/Hero/Hero";

const AdminPanel = () => {
  return (
    <div>
      <Hero title="ADMIN PANEL" cName="hero__img" />
      <div style={{ textAlign: "center", margin: "2rem" }}>
        <h2>Welcome to the Admin Panel</h2>
        <p>
          This is the administrative area. For now, it only displays a banner
          and minimal content.
        </p>
      </div>
    </div>
  );
};

export default AdminPanel; // Dodanie eksportu domyślnego
