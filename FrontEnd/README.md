# WikiFace Frontend

A sleek, modern landing page for the WikiFace project featuring a dark theme and dynamic animations.

## Features

- **Dark Theme**: Modern dark color scheme with purple/blue gradients
- **Responsive Design**: Fully responsive across all device sizes
- **Smooth Animations**: CSS animations and JavaScript interactions
- **Interactive Elements**: Hover effects, scroll animations, and particle effects
- **Team Showcase**: Displays team members side by side as requested

## Files Structure

```
FrontEnd/
├── index.html          # Main landing page
├── styles.css          # Dark theme styling and animations
├── script.js           # Interactive functionality
└── README.md           # This file
```

## Team Members

The landing page showcases the three team members side by side:

- **Atharva Walavalkar** - AI & Machine Learning
- **Yash Malode** - Backend Development  
- **Jaison Menenzes** - Frontend & UI/UX

## How to Use

1. **Open the landing page**: Simply open `index.html` in any modern web browser
2. **Local Development**: You can serve it locally using any HTTP server:
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js (if you have http-server installed)
   npx http-server
   
   # Using PHP
   php -S localhost:8000
   ```

3. **View Online**: Upload the files to any web hosting service

## Customization

### Colors
The color scheme is defined in CSS variables at the top of `styles.css`:
```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --bg-primary: #0f0f23;
    --bg-secondary: #1a1a2e;
    /* ... more variables */
}
```

### Content
- Update team member information in `index.html`
- Modify project description and features
- Change statistics in the About section
- Update social media links in the footer

### Animations
- Adjust animation timing in `script.js`
- Modify particle effects
- Change hover animations in `styles.css`

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Technologies Used

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid, Flexbox, and animations
- **JavaScript (ES6+)**: Interactive functionality
- **Font Awesome**: Icons
- **Google Fonts**: Inter font family

## Performance

- Optimized animations using CSS transforms
- Efficient JavaScript with event delegation
- Minimal external dependencies
- Responsive images and lazy loading ready

## Future Enhancements

- Add a mobile menu for smaller screens
- Implement a blog section
- Add a contact form
- Include a demo section showing actual WikiFace functionality
- Add more interactive elements like model showcases 