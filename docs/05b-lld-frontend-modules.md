# Low-Level Design - Frontend Modules (React)

**Document**: Phase 4b - Frontend Implementation Specifications  
**Migration**: OpenCart PHP Views → React SPA Frontend  
**Version**: 1.0  
**Date**: 2025-01-19

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Component Hierarchy](#component-hierarchy)
3. [Page Components](#page-components)
4. [Routing Strategy](#routing-strategy)
5. [State Management](#state-management)
6. [API Integration](#api-integration)
7. [Form Handling](#form-handling)
8. [UX Parity Mapping](#ux-parity-mapping)

---

## Project Structure

### Directory Organization

```
opencart-modern-frontend-react-307441/
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── assets/
│       └── images/
│
├── src/
│   ├── index.js                      # Application entry point
│   ├── App.js                        # Root component
│   │
│   ├── pages/
│   │   ├── HomePage.js               # Landing page
│   │   ├── ProductListPage.js        # Product catalog
│   │   ├── ProductDetailPage.js      # Product detail
│   │   ├── CategoryPage.js           # Category browse
│   │   ├── SearchResultsPage.js      # Search results
│   │   ├── CartPage.js               # Shopping cart
│   │   ├── CheckoutPage.js           # Checkout flow
│   │   ├── OrderSuccessPage.js       # Order confirmation
│   │   ├── LoginPage.js              # Customer login
│   │   ├── RegisterPage.js           # Customer registration
│   │   ├── AccountPage.js            # Customer dashboard
│   │   ├── OrderHistoryPage.js       # Order history
│   │   ├── AccountAddressesPage.js   # Address management
│   │   ├── NotFoundPage.js           # 404 error
│   │   │
│   │   └── admin/
│   │       ├── AdminDashboard.js
│   │       ├── AdminProductsPage.js
│   │       ├── AdminOrdersPage.js
│   │       └── AdminCustomersPage.js
│   │
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.js             # Site header
│   │   │   ├── Footer.js             # Site footer
│   │   │   ├── Navigation.js         # Main navigation
│   │   │   ├── Breadcrumb.js         # Breadcrumb trail
│   │   │   ├── Pagination.js         # Pagination controls
│   │   │   ├── LoadingSpinner.js     # Loading indicator
│   │   │   ├── ErrorMessage.js       # Error display
│   │   │   └── Modal.js              # Modal dialog
│   │   │
│   │   ├── product/
│   │   │   ├── ProductCard.js        # Product list item
│   │   │   ├── ProductGrid.js        # Product grid layout
│   │   │   ├── ProductFilter.js      # Filter controls
│   │   │   ├── ProductSort.js        # Sort controls
│   │   │   ├── ProductSearch.js      # Search bar
│   │   │   ├── ProductImages.js      # Image gallery
│   │   │   ├── ProductOptions.js     # Product options selector
│   │   │   ├── ProductReviews.js     # Reviews list
│   │   │   └── AddToCartButton.js    # Add to cart
│   │   │
│   │   ├── cart/
│   │   │   ├── CartIcon.js           # Header cart badge
│   │   │   ├── CartItem.js           # Cart item row
│   │   │   ├── CartSummary.js        # Cart totals
│   │   │   └── CartEmpty.js          # Empty cart message
│   │   │
│   │   ├── checkout/
│   │   │   ├── CheckoutSteps.js      # Step indicator
│   │   │   ├── ShippingAddressForm.js
│   │   │   ├── PaymentAddressForm.js
│   │   │   ├── ShippingMethodSelect.js
│   │   │   ├── PaymentMethodSelect.js
│   │   │   └── OrderReview.js
│   │   │
│   │   ├── category/
│   │   │   ├── CategoryMenu.js       # Category navigation
│   │   │   └── CategoryTree.js       # Hierarchical category
│   │   │
│   │   └── account/
│   │       ├── LoginForm.js
│   │       ├── RegisterForm.js
│   │       ├── ProfileForm.js
│   │       ├── AddressForm.js
│   │       └── OrderCard.js
│   │
│   ├── services/
│   │   ├── api.js                    # Axios config
│   │   ├── productService.js         # Product API calls
│   │   ├── cartService.js            # Cart API calls
│   │   ├── orderService.js           # Order API calls
│   │   ├── customerService.js        # Customer API calls
│   │   ├── authService.js            # Auth API calls
│   │   └── categoryService.js        # Category API calls
│   │
│   ├── context/
│   │   ├── AuthContext.js            # Authentication state
│   │   ├── CartContext.js            # Shopping cart state
│   │   └── NotificationContext.js    # Notifications/toasts
│   │
│   ├── hooks/
│   │   ├── useAuth.js                # Auth hook
│   │   ├── useCart.js                # Cart hook
│   │   ├── useApi.js                 # API call hook
│   │   ├── useForm.js                # Form handling hook
│   │   └── useDebounce.js            # Debounce hook
│   │
│   ├── utils/
│   │   ├── formatters.js             # Price, date formatting
│   │   ├── validators.js             # Form validation
│   │   ├── constants.js              # App constants
│   │   └── helpers.js                # Utility functions
│   │
│   ├── routes/
│   │   ├── AppRoutes.js              # Route definitions
│   │   └── ProtectedRoute.js         # Auth-protected route
│   │
│   └── styles/
│       ├── global.css                # Global styles
│       ├── theme.css                 # Theme variables
│       └── responsive.css            # Media queries
│
├── package.json
├── .env
└── .env.example
```

---

## Component Hierarchy

### Application Component Tree

```
App
├── Router
│   ├── Header
│   │   ├── Logo
│   │   ├── Navigation
│   │   │   └── CategoryMenu
│   │   ├── ProductSearch
│   │   ├── CartIcon
│   │   └── AccountMenu
│   │
│   ├── Routes
│   │   ├── HomePage
│   │   │   ├── HeroBanner
│   │   │   ├── FeaturedProducts
│   │   │   └── CategoryShowcase
│   │   │
│   │   ├── ProductListPage
│   │   │   ├── Breadcrumb
│   │   │   ├── ProductFilter
│   │   │   ├── ProductSort
│   │   │   ├── ProductGrid
│   │   │   │   └── ProductCard (multiple)
│   │   │   └── Pagination
│   │   │
│   │   ├── ProductDetailPage
│   │   │   ├── Breadcrumb
│   │   │   ├── ProductImages
│   │   │   ├── ProductInfo
│   │   │   ├── ProductOptions
│   │   │   ├── AddToCartButton
│   │   │   ├── ProductDescription
│   │   │   └── ProductReviews
│   │   │
│   │   ├── CartPage
│   │   │   ├── CartEmpty (conditional)
│   │   │   ├── CartItem (multiple)
│   │   │   ├── CartSummary
│   │   │   └── CheckoutButton
│   │   │
│   │   └── CheckoutPage
│   │       ├── CheckoutSteps
│   │       ├── ShippingAddressForm
│   │       ├── ShippingMethodSelect
│   │       ├── PaymentAddressForm
│   │       ├── PaymentMethodSelect
│   │       ├── OrderReview
│   │       └── PlaceOrderButton
│   │
│   └── Footer
│       ├── FooterLinks
│       └── Copyright
```

---

## Page Components

### Home Page

**Component**: `HomePage.js`

**Purpose**: Landing page with featured products and category showcase

**PHP Template Equivalent**: `catalog/view/template/common/home.twig`

**Key Elements**:
- Hero banner/slider
- Featured products grid
- Category showcase
- Special offers section

**Data Requirements**:
- Featured products from API
- Categories with images
- Banner content

**State**:
```javascript
const [featuredProducts, setFeaturedProducts] = useState([]);
const [categories, setCategories] = useState([]);
const [loading, setLoading] = useState(true);
```

**API Calls**:
```javascript
useEffect(() => {
  Promise.all([
    productService.getFeatured(),
    categoryService.getAll()
  ]).then(([products, cats]) => {
    setFeaturedProducts(products);
    setCategories(cats);
    setLoading(false);
  });
}, []);
```

---

### Product List Page

**Component**: `ProductListPage.js`

**Purpose**: Display paginated product catalog with filtering and sorting

**PHP Template Equivalent**: `catalog/view/template/product/category.twig`

**Key Elements**:
- Breadcrumb navigation
- Filter sidebar (price, manufacturer, options)
- Sort dropdown
- Product grid
- Pagination controls

**State**:
```javascript
const [products, setProducts] = useState([]);
const [filters, setFilters] = useState({
  category_id: null,
  min_price: null,
  max_price: null,
  manufacturer: null
});
const [sort, setSort] = useState('sort_order');
const [order, setOrder] = useState('asc');
const [page, setPage] = useState(1);
const [totalPages, setTotalPages] = useState(1);
```

**API Integration**:
```javascript
useEffect(() => {
  productService.getProducts({
    category_id: filters.category_id,
    sort,
    order,
    page,
    limit: 20
  }).then(response => {
    setProducts(response.items);
    setTotalPages(response.pages);
  });
}, [filters, sort, order, page]);
```

---

### Product Detail Page

**Component**: `ProductDetailPage.js`

**Purpose**: Display detailed product information and purchase options

**PHP Template Equivalent**: `catalog/view/template/product/product.twig`

**Key Elements**:
- Image gallery with zoom
- Product title, model, price
- Product description
- Options selector (size, color, etc.)
- Quantity input
- Add to cart button
- Reviews and ratings
- Related products

**State**:
```javascript
const [product, setProduct] = useState(null);
const [selectedOptions, setSelectedOptions] = useState({});
const [quantity, setQuantity] = useState(1);
const [images, setImages] = useState([]);
const [activeImage, setActiveImage] = useState(0);
```

**Add to Cart Logic**:
```javascript
const handleAddToCart = async () => {
  try {
    await cartService.addItem({
      product_id: product.product_id,
      quantity,
      options: selectedOptions
    });
    
    // Update cart context
    await refreshCart();
    
    // Show success notification
    showNotification('Product added to cart');
  } catch (error) {
    showNotification('Failed to add to cart', 'error');
  }
};
```

---

### Cart Page

**Component**: `CartPage.js`

**Purpose**: Display cart contents and allow quantity updates

**PHP Template Equivalent**: `catalog/view/template/checkout/cart.twig`

**Key Elements**:
- Cart items list
- Quantity controls
- Remove item button
- Cart totals (subtotal, shipping, tax, total)
- Continue shopping button
- Checkout button

**State** (from CartContext):
```javascript
const { cart, updateQuantity, removeItem, loading } = useCart();
```

**Component Structure**:
```javascript
return (
  <div className="cart-page">
    {cart.items.length === 0 ? (
      <CartEmpty />
    ) : (
      <>
        <div className="cart-items">
          {cart.items.map(item => (
            <CartItem
              key={item.cart_id}
              item={item}
              onUpdateQuantity={updateQuantity}
              onRemove={removeItem}
            />
          ))}
        </div>
        
        <CartSummary totals={cart.totals} />
        
        <button onClick={() => navigate('/checkout')}>
          Proceed to Checkout
        </button>
      </>
    )}
  </div>
);
```

---

### Checkout Page

**Component**: `CheckoutPage.js`

**Purpose**: Multi-step checkout flow

**PHP Template Equivalent**: `catalog/view/template/checkout/checkout.twig`

**Steps**:
1. Shipping Address
2. Shipping Method
3. Payment Address
4. Payment Method
5. Order Review

**State**:
```javascript
const [currentStep, setCurrentStep] = useState(1);
const [shippingAddress, setShippingAddress] = useState({});
const [paymentAddress, setPaymentAddress] = useState({});
const [shippingMethod, setShippingMethod] = useState(null);
const [paymentMethod, setPaymentMethod] = useState(null);
const [shippingMethods, setShippingMethods] = useState([]);
const [paymentMethods, setPaymentMethods] = useState([]);
```

**Step Navigation**:
```javascript
const handleNextStep = async () => {
  if (currentStep === 1) {
    // Validate shipping address
    if (!validateAddress(shippingAddress)) return;
    
    // Fetch shipping methods
    const methods = await checkoutService.getShippingMethods(shippingAddress);
    setShippingMethods(methods);
  }
  
  setCurrentStep(currentStep + 1);
};
```

**Order Placement**:
```javascript
const handlePlaceOrder = async () => {
  try {
    const orderData = {
      shipping_address: shippingAddress,
      payment_address: paymentAddress,
      shipping_method: shippingMethod,
      payment_method: paymentMethod
    };
    
    const response = await orderService.createOrder(orderData);
    
    navigate(`/checkout/success/${response.order_id}`);
  } catch (error) {
    showNotification('Order placement failed', 'error');
  }
};
```

---

### Account Pages

**Login Page** (`LoginPage.js`)

**PHP Equivalent**: `catalog/view/template/account/login.twig`

```javascript
const LoginPage = () => {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      await login(email, password);
      navigate('/account');
    } catch (err) {
      setError('Invalid email or password');
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      {error && <div className="error">{error}</div>}
      <button type="submit">Login</button>
    </form>
  );
};
```

**Register Page** (`RegisterPage.js`)

**PHP Equivalent**: `catalog/view/template/account/register.twig`

Similar structure with additional fields (firstname, lastname, telephone).

**Account Dashboard** (`AccountPage.js`)

**PHP Equivalent**: `catalog/view/template/account/account.twig`

Links to:
- Edit profile
- View orders
- Manage addresses
- Change password

---

## Routing Strategy

### React Router Configuration

**File**: `src/routes/AppRoutes.js`

```javascript
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';

// Page imports
import HomePage from '../pages/HomePage';
import ProductListPage from '../pages/ProductListPage';
import ProductDetailPage from '../pages/ProductDetailPage';
import CartPage from '../pages/CartPage';
import CheckoutPage from '../pages/CheckoutPage';
import LoginPage from '../pages/LoginPage';
import RegisterPage from '../pages/RegisterPage';
import AccountPage from '../pages/AccountPage';
import OrderHistoryPage from '../pages/OrderHistoryPage';
import NotFoundPage from '../pages/NotFoundPage';

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/products" element={<ProductListPage />} />
        <Route path="/products/:id" element={<ProductDetailPage />} />
        <Route path="/category/:id" element={<ProductListPage />} />
        <Route path="/search" element={<ProductListPage />} />
        <Route path="/cart" element={<CartPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        
        {/* Protected routes */}
        <Route
          path="/checkout"
          element={
            <ProtectedRoute>
              <CheckoutPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/account"
          element={
            <ProtectedRoute>
              <AccountPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/account/orders"
          element={
            <ProtectedRoute>
              <OrderHistoryPage />
            </ProtectedRoute>
          }
        />
        
        {/* 404 */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;
```

### Protected Route Component

**File**: `src/routes/ProtectedRoute.js`

```javascript
import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <LoadingSpinner />;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

export default ProtectedRoute;
```

---

## State Management

### Context API Implementation

**Auth Context** (`src/context/AuthContext.js`)

```javascript
import { createContext, useState, useEffect } from 'react';
import authService from '../services/authService';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Check for existing token on mount
    const token = localStorage.getItem('access_token');
    
    if (token) {
      authService.verifyToken(token).then(user => {
        setUser(user);
        setIsAuthenticated(true);
        setLoading(false);
      }).catch(() => {
        localStorage.removeItem('access_token');
        setLoading(false);
      });
    } else {
      setLoading(false);
    }
  }, []);
  
  const login = async (email, password) => {
    const response = await authService.login(email, password);
    
    localStorage.setItem('access_token', response.access_token);
    setUser(response.customer);
    setIsAuthenticated(true);
  };
  
  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    setIsAuthenticated(false);
  };
  
  const register = async (userData) => {
    const response = await authService.register(userData);
    
    localStorage.setItem('access_token', response.access_token);
    setUser(response.customer);
    setIsAuthenticated(true);
  };
  
  return (
    <AuthContext.Provider value={{ user, isAuthenticated, loading, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};
```

**Cart Context** (`src/context/CartContext.js`)

```javascript
import { createContext, useState, useEffect } from 'react';
import cartService from '../services/cartService';
import { useAuth } from '../hooks/useAuth';

export const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const [cart, setCart] = useState({ items: [], totals: [] });
  const [itemCount, setItemCount] = useState(0);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    if (isAuthenticated) {
      refreshCart();
    }
  }, [isAuthenticated]);
  
  const refreshCart = async () => {
    setLoading(true);
    try {
      const cartData = await cartService.getCart();
      setCart(cartData);
      setItemCount(cartData.items.reduce((sum, item) => sum + item.quantity, 0));
    } catch (error) {
      console.error('Failed to load cart', error);
    }
    setLoading(false);
  };
  
  const addItem = async (product_id, quantity, options) => {
    await cartService.addItem({ product_id, quantity, options });
    await refreshCart();
  };
  
  const updateQuantity = async (cart_id, quantity) => {
    await cartService.updateItem(cart_id, { quantity });
    await refreshCart();
  };
  
  const removeItem = async (cart_id) => {
    await cartService.removeItem(cart_id);
    await refreshCart();
  };
  
  const clearCart = async () => {
    await cartService.clearCart();
    setCart({ items: [], totals: [] });
    setItemCount(0);
  };
  
  return (
    <CartContext.Provider value={{
      cart,
      itemCount,
      loading,
      addItem,
      updateQuantity,
      removeItem,
      clearCart,
      refreshCart
    }}>
      {children}
    </CartContext.Provider>
  );
};
```

---

## API Integration

### Axios Configuration

**File**: `src/services/api.js`

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor - add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    
    return Promise.reject(error.response?.data || error.message);
  }
);

export default api;
```

### Service Modules

**Product Service** (`src/services/productService.js`)

```javascript
import api from './api';

const productService = {
  getProducts: (params) => {
    return api.get('/products', { params });
  },
  
  getProduct: (id) => {
    return api.get(`/products/${id}`);
  },
  
  getFeatured: () => {
    return api.get('/products?featured=true');
  },
  
  searchProducts: (query) => {
    return api.get('/products', { params: { search: query } });
  }
};

export default productService;
```

**Cart Service** (`src/services/cartService.js`)

```javascript
import api from './api';

const cartService = {
  getCart: () => {
    return api.get('/cart');
  },
  
  addItem: (data) => {
    return api.post('/cart/items', data);
  },
  
  updateItem: (cart_id, data) => {
    return api.put(`/cart/items/${cart_id}`, data);
  },
  
  removeItem: (cart_id) => {
    return api.delete(`/cart/items/${cart_id}`);
  },
  
  clearCart: () => {
    return api.delete('/cart');
  }
};

export default cartService;
```

---

## Form Handling

### Custom Form Hook

**File**: `src/hooks/useForm.js`

```javascript
import { useState } from 'react';

const useForm = (initialValues, validationRules) => {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  
  const handleChange = (name, value) => {
    setValues({ ...values, [name]: value });
    
    // Validate field if touched
    if (touched[name]) {
      const error = validateField(name, value, validationRules);
      setErrors({ ...errors, [name]: error });
    }
  };
  
  const handleBlur = (name) => {
    setTouched({ ...touched, [name]: true });
    
    const error = validateField(name, values[name], validationRules);
    setErrors({ ...errors, [name]: error });
  };
  
  const validateField = (name, value, rules) => {
    const rule = rules[name];
    
    if (!rule) return null;
    
    if (rule.required && !value) {
      return rule.requiredMessage || 'This field is required';
    }
    
    if (rule.minLength && value.length < rule.minLength) {
      return `Minimum ${rule.minLength} characters required`;
    }
    
    if (rule.pattern && !rule.pattern.test(value)) {
      return rule.patternMessage || 'Invalid format';
    }
    
    return null;
  };
  
  const validateAll = () => {
    const newErrors = {};
    
    Object.keys(validationRules).forEach(name => {
      const error = validateField(name, values[name], validationRules);
      if (error) newErrors[name] = error;
    });
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const reset = () => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
  };
  
  return {
    values,
    errors,
    touched,
    handleChange,
    handleBlur,
    validateAll,
    reset
  };
};

export default useForm;
```

### Example Form Usage

**Address Form Component** (`src/components/account/AddressForm.js`)

```javascript
import useForm from '../../hooks/useForm';

const AddressForm = ({ onSubmit, initialData = {} }) => {
  const { values, errors, touched, handleChange, handleBlur, validateAll } = useForm(
    {
      firstname: initialData.firstname || '',
      lastname: initialData.lastname || '',
      address_1: initialData.address_1 || '',
      city: initialData.city || '',
      postcode: initialData.postcode || '',
      country_id: initialData.country_id || '',
      zone_id: initialData.zone_id || ''
    },
    {
      firstname: { required: true, requiredMessage: 'First name is required' },
      lastname: { required: true, requiredMessage: 'Last name is required' },
      address_1: { required: true, requiredMessage: 'Address is required' },
      city: { required: true, requiredMessage: 'City is required' },
      postcode: { 
        required: true, 
        pattern: /^\d{5}$/,
        patternMessage: 'Invalid postal code'
      }
    }
  );
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateAll()) {
      onSubmit(values);
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          type="text"
          value={values.firstname}
          onChange={(e) => handleChange('firstname', e.target.value)}
          onBlur={() => handleBlur('firstname')}
          placeholder="First Name"
        />
        {touched.firstname && errors.firstname && (
          <span className="error">{errors.firstname}</span>
        )}
      </div>
      
      {/* Similar fields for other inputs */}
      
      <button type="submit">Save Address</button>
    </form>
  );
};
```

---

## UX Parity Mapping

### PHP View to React Component Mapping

| PHP Template | React Component | Key Features Preserved |
|-------------|-----------------|----------------------|
| `common/home.twig` | `HomePage.js` | Featured products, category showcase |
| `product/category.twig` | `ProductListPage.js` | Filtering, sorting, pagination |
| `product/product.twig` | `ProductDetailPage.js` | Image gallery, options, add to cart |
| `checkout/cart.twig` | `CartPage.js` | Item list, quantity update, totals |
| `checkout/checkout.twig` | `CheckoutPage.js` | Multi-step flow, address forms |
| `account/login.twig` | `LoginPage.js` | Email/password login form |
| `account/register.twig` | `RegisterPage.js` | Registration form validation |
| `account/account.twig` | `AccountPage.js` | Account dashboard links |
| `account/order.twig` | `OrderHistoryPage.js` | Order list, detail view |

### Behavior Preservation Checklist

**Product Browsing**:
- ✅ Same filtering options (price, manufacturer)
- ✅ Same sorting options (name, price, date)
- ✅ Same pagination (20 items per page)
- ✅ Same product card information (image, name, price, rating)

**Product Detail**:
- ✅ Image gallery with thumbnails
- ✅ Product options with price modifiers
- ✅ Quantity selector with min/max validation
- ✅ Add to cart with option validation
- ✅ Reviews display with rating

**Cart**:
- ✅ Item quantity update
- ✅ Item removal
- ✅ Totals calculation (subtotal, shipping, tax, total)
- ✅ Empty cart message
- ✅ Continue shopping link

**Checkout**:
- ✅ Multi-step process (same steps as PHP)
- ✅ Address validation
- ✅ Shipping method selection
- ✅ Payment method selection
- ✅ Order review before placement

**Account**:
- ✅ Login with email/password
- ✅ Registration with all required fields
- ✅ Order history display
- ✅ Address management

---

## Summary

This Low-Level Design document provides comprehensive specifications for implementing the React frontend, including:

- **Project Structure**: Organized by feature with clear separation of pages, components, services
- **Component Hierarchy**: Complete component tree from App root to leaf components
- **Page Components**: Detailed specs for all major pages with state management
- **Routing Strategy**: React Router configuration with protected routes
- **State Management**: Context API for global state (auth, cart)
- **API Integration**: Axios-based service layer with interceptors
- **Form Handling**: Custom hook for form validation and management
- **UX Parity Mapping**: Complete mapping from PHP views to React components

All implementations must maintain 100% functional parity with the original PHP OpenCart storefront while providing a modern, responsive user experience.

---

**Next Document**: [06-migration-plan.md](./06-migration-plan.md) - Migration execution strategy
