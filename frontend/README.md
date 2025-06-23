# Electricity Market Simulation Platform - Frontend

A modern Vue.js frontend for the Electricity Market Simulation Platform.

## Features

- **Multi-page Routing**: Complete SPA with Vue Router
- **User Authentication**: Login/Register with JWT tokens
- **Role-based Access**: Separate interfaces for students and teachers
- **Real-time Bidding**: Interactive bidding interface
- **Data Visualization**: ECharts integration for results analysis
- **Responsive Design**: Bootstrap 5 for modern UI
- **Class Management**: Teachers can manage classes and students
- **Profile Management**: User profile and password management

## Pages

- **Login/Register**: User authentication
- **Dashboard**: Overview of user activities and statistics
- **Scenarios**: View and join experiment scenarios
- **Bidding**: Submit bids for active scenarios
- **Results**: Analyze simulation results with charts
- **Profile**: Manage personal information and password
- **Admin Panel**: Teacher-only scenario management
- **Class Management**: Teacher-only class and student management

## Technology Stack

- **Vue 3**: Progressive JavaScript framework
- **Vue Router 4**: Official router for Vue.js
- **Axios**: HTTP client for API communication
- **ECharts**: Data visualization library
- **Bootstrap 5**: CSS framework for responsive design
- **Vite**: Fast build tool and dev server

## Quick Start

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend server running on http://localhost:8000

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and visit:
   ```
   http://localhost:3000
   ```

### Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable components
│   │   └── Layout.vue       # Main layout with sidebar
│   │   ├── Login.vue        # Authentication
│   │   ├── Dashboard.vue    # Overview dashboard
│   │   ├── Scenarios.vue    # Scenario management
│   │   ├── Bidding.vue      # Bidding interface
│   │   ├── Results.vue      # Results analysis
│   │   ├── Profile.vue      # User profile
│   │   ├── AdminPanel.vue   # Teacher admin panel
│   │   └── ClassManagement.vue # Class management
│   │   └── Layout.vue       # Main layout with sidebar
│   ├── views/               # Page components
│   ├── services/            # API services
│   │   └── api.js           # Axios configuration
│   ├── router/              # Vue Router configuration
│   │   └── index.js         # Route definitions
│   ├── assets/              # Static assets
│   │   └── main.css         # Global styles
│   ├── App.vue              # Root component
│   └── main.js              # Application entry point
├── index.html               # HTML template
├── package.json             # Dependencies and scripts
├── vite.config.js           # Vite configuration
└── README.md                # This file
```

## API Integration

The frontend communicates with the backend API through the `api.js` service:

- **Base URL**: http://localhost:8000
- **Authentication**: JWT tokens stored in localStorage
- **Error Handling**: Automatic token refresh and error responses
- **CORS**: Configured for development and production

## Key Features

### Authentication
- JWT-based authentication
- Automatic token refresh
- Role-based route protection
- Persistent login state

### Real-time Updates
- Live scenario status updates
- Real-time bidding interface
- Dynamic result calculations

### Data Visualization
- Supply and demand curves
- Market clearing price visualization
- Participant performance charts
- Interactive ECharts integration

### User Management
- Profile information updates
- Password change functionality
- User statistics tracking
- Class enrollment management

## Development

### Adding New Pages

1. Create a new Vue component in `src/views/`
2. Add the route in `src/router/index.js`
3. Update the navigation in `src/components/Layout.vue`

### Styling

- Global styles in `src/assets/main.css`
- Bootstrap 5 classes for responsive design
- Custom CSS classes for specific components

### API Calls

Use the `api.js` service for all HTTP requests:

```javascript
import api from '../services/api.js'

// GET request
const response = await api.get('/endpoint')

// POST request
const response = await api.post('/endpoint', data)

// PUT request
const response = await api.put('/endpoint', data)

// DELETE request
const response = await api.delete('/endpoint')
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure backend CORS is configured correctly
2. **Authentication Issues**: Check JWT token validity and expiration
3. **Build Errors**: Verify Node.js version and dependencies
4. **API Connection**: Confirm backend server is running on port 8000

### Development Tips

- Use Vue DevTools for debugging
- Check browser console for API errors
- Monitor network tab for request/response details
- Use localStorage to inspect authentication state

## Contributing

1. Follow Vue.js best practices
2. Use consistent code formatting
3. Add comments for complex logic
4. Test all user flows before committing
5. Update documentation for new features 