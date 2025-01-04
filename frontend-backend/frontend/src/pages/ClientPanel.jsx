import Hero from "../components/Hero/Hero";

const ClientPanel = () => {
  return (
    <div>
      <Hero title="CLIENT PANEL" cName="hero__img" />
      <div style={{ textAlign: "center", margin: "2rem" }}>
        <h2>Your Orders</h2>
        <p>
          This is the client panel. For now, it only displays a banner and
          minimal content.
        </p>
      </div>
    </div>
  );
};

export default ClientPanel; // Dodanie eksportu domyślnego
