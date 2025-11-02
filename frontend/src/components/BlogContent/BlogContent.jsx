/**
 * BlogContent Component
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2025-11-02
 * Version: 2.0
 *
 * Blog listing component displaying articles about technology and gadgets.
 * Shows grid of blog post previews with navigation to full articles.
 *
 * Features:
 *   - Grid layout of blog posts
 *   - Article previews with images
 *   - Read more links to full articles
 *   - Responsive design
 *   - Static content from data file
 *
 * Content Structure:
 *   - Each blog item includes:
 *     * Title
 *     * Excerpt/preview text
 *     * Featured image
 *     * Publication date
 *     * Author information
 *     * Category tags
 *     * Read more link
 *
 * Data Source:
 *   - BlogData.js - Array of blog post objects
 *   - Each item: {id, title, excerpt, image, date, author, category, ...}
 *
 * Navigation:
 *   - BlogItem component handles routing to /blog/:id
 *
 * @component
 * @returns {React.ReactElement} Blog posts grid section
 */
import "./BlogContent.scss";
import blogData from "./BlogData";
import BlogItem from "./BlogItem";

const BlogContent = () => {
  return (
    <section className="blog">
      <h2 className="blog__heading">Discover the Latest in Tech and Gadgets</h2>
      <div className="blog__body container">
        {blogData.map((item) => (
          <BlogItem {...item} key={item.id} />
        ))}
      </div>
    </section>
  );
};

export default BlogContent;
