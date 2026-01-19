# Current Implementation - PHP OpenCart

**Document Version**: 1.0  
**Last Updated**: 2025-01-19  
**Purpose**: Comprehensive analysis of the legacy OpenCart 3.0.7.4 PHP implementation

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Technology Stack](#technology-stack)
3. [Folder Structure](#folder-structure)
4. [Runtime Behavior](#runtime-behavior)
5. [Business Flows](#business-flows)
6. [PHP Execution Model](#php-execution-model)

---

## System Overview

### What is OpenCart?

OpenCart is a **free, open-source e-commerce platform** built in PHP, designed for online merchants to create and manage professional online stores. Version 3.0.7.4 represents a mature implementation with extensive features for:

- Product catalog management
- Shopping cart and checkout flows
- Customer account management
- Order processing and tracking
- Multi-store and multi-language support
- Extension system for payments, shipping, themes

### Core Capabilities

**Catalog Management:**
- Hierarchical product categories with unlimited depth
- Product variants with options (size, color, etc.)
- Product attributes, filters, and custom fields
- Manufacturer/brand management
- Product reviews and ratings
- Special pricing, discounts, and promotions
- Downloadable products

**Customer Features:**
- User registration and authentication
- Customer groups with different pricing
- Address management (billing/shipping)
- Wishlist and product comparison
- Order history and reordering
- Reward points and affiliate programs
- Customer reviews and product tracking

**Checkout & Orders:**
- Multi-step checkout process
- Guest and registered customer checkout
- Multiple payment methods (bank transfer, COD, cheque, free checkout)
- Multiple shipping methods (flat rate, weight-based, pickup, free)
- Tax calculations (VAT, sales tax)
- Coupon and voucher support
- Order status tracking and email notifications

**Admin Panel:**
- Comprehensive dashboard with analytics
- Product, category, and inventory management
- Customer and order management
- Sales reports and statistics
- Extension management (modules, payments, shipping)
- Settings and configuration management
- User roles and permissions

---

## Technology Stack

### Core Technologies

**Backend Language:**
- **PHP 8.0+** (minimum requirement, 8.4 supported)
- Namespaced architecture (`Opencart\Catalog\`, `Opencart\Admin\`, `Opencart\System\`)
- Object-oriented programming with MVC pattern

**Database:**
- **MySQL 5.7+** or **MariaDB 10.3+**
- Direct SQL queries (no ORM)
- Database abstraction layer supporting MySQLi, PDO, PostgreSQL

**Web Server:**
- **Apache 2.4+** with mod_rewrite
- **Nginx** (alternative configuration)
- URL rewriting for SEO-friendly URLs

**Template Engine:**
- **Twig 3.x** for view rendering
- Server-side rendering (SSR)
- Template inheritance and includes

### Supporting Libraries

**Frontend Assets:**
- **jQuery 3.7.1** for JavaScript functionality
- **Bootstrap 5.x** for UI framework
- **Font Awesome 6.x** for icons
- Custom JavaScript for product interactions

**Additional PHP Libraries:**
- **Composer** for dependency management
- **PHPStan** for static analysis
- **PHP-CS-Fixer** for code standards
- **SCSS/SASS** for stylesheet compilation

### Development Environment

**Docker Support:**
- Multi-container setup (Apache, PHP-FPM, MySQL, Redis, Memcached)
- Docker Compose profiles for optional services
- WSL2 recommended for Windows development

**Caching:**
- File-based caching (default)
- Redis support (optional)
- Memcached support (optional)
- APCU support (optional)

---

## Folder Structure

### Root Directory Layout

```
opencart-307441/
├── upload/                      # Main application directory
│   ├── admin/                   # Admin panel application
│   ├── catalog/                 # Customer-facing storefront
│   ├── extension/               # Extensions and modules
│   ├── image/                   # Product and content images
│   ├── install/                 # Installation wizard
│   ├── system/                  # Core framework code
│   ├── config-dist.php          # Configuration template
│   └── index.php                # Frontend entry point
├── docs/                        # API documentation
├── docker/                      # Docker configuration
├── tools/                       # Development tools
├── INSTALL.md                   # Installation instructions
├── UPGRADE.md                   # Upgrade instructions
├── README.md                    # Project documentation
└── composer.json                # PHP dependencies
```

### Catalog (Storefront) Structure

```
upload/catalog/
├── controller/                  # MVC Controllers
│   ├── account/                 # Customer account pages
│   ├── checkout/                # Checkout process
│   ├── product/                 # Product display
│   ├── common/                  # Shared components (header, footer)
│   ├── information/             # Static pages
│   └── api/                     # API endpoints
├── model/                       # MVC Models (data access)
│   ├── account/                 # Customer data models
│   ├── catalog/                 # Product/category models
│   ├── checkout/                # Order/cart models
│   └── localisation/            # Localization data
├── view/                        # MVC Views (templates)
│   ├── template/                # Twig templates
│   ├── javascript/              # Frontend JavaScript
│   ├── stylesheet/              # CSS files
│   └── fonts/                   # Web fonts
└── language/                    # Translation files
    ├── en-gb/                   # English (UK)
    └── fr-fr/                   # French
```

### Admin Panel Structure

```
upload/admin/
├── controller/                  # Admin controllers
│   ├── catalog/                 # Product/category management
│   ├── customer/                # Customer management
│   ├── sale/                    # Order management
│   ├── extension/               # Extension management
│   ├── marketplace/             # Extension marketplace
│   └── common/                  # Dashboard, login
├── model/                       # Admin data models
│   ├── catalog/                 # Product CRUD operations
│   ├── customer/                # Customer CRUD operations
│   └── sale/                    # Order CRUD operations
├── view/                        # Admin templates
│   └── template/                # Twig admin templates
└── language/                    # Admin translations
```

### System (Core Framework) Structure

```
upload/system/
├── engine/                      # Core framework classes
│   ├── action.php               # Action dispatcher
│   ├── controller.php           # Base controller
│   ├── model.php                # Base model
│   ├── registry.php             # Dependency injection container
│   ├── loader.php               # Dynamic loader
│   └── event.php                # Event system
├── library/                     # Framework libraries
│   ├── db/                      # Database abstraction
│   ├── cache/                   # Caching implementations
│   ├── cart/                    # Shopping cart logic
│   ├── session/                 # Session management
│   ├── mail/                    # Email functionality
│   └── template/                # Template engine (Twig)
└── helper/                      # Utility functions
    ├── general.php              # General helpers
    ├── utf8.php                 # UTF-8 string functions
    └── validation.php           # Validation helpers
```

### Extension Structure

```
upload/extension/opencart/
├── admin/                       # Admin-side extensions
│   ├── controller/
│   │   ├── payment/             # Payment method configs
│   │   ├── shipping/            # Shipping method configs
│   │   ├── module/              # Module configurations
│   │   └── dashboard/           # Dashboard widgets
│   ├── model/                   # Extension models
│   └── view/                    # Extension templates
└── catalog/                     # Catalog-side extensions
    ├── controller/
    │   ├── payment/             # Payment processors
    │   ├── shipping/            # Shipping calculators
    │   └── module/              # Frontend modules
    └── model/                   # Extension data access
```

---

## Runtime Behavior

### Request Lifecycle

#### 1. Entry Point

**Catalog (Storefront):**
```
HTTP Request → upload/index.php
```

**Admin Panel:**
```
HTTP Request → upload/admin/index.php
```

#### 2. Bootstrap Process

```php
// index.php simplified flow
1. Define constants (DIR_APPLICATION, DIR_SYSTEM, etc.)
2. Load configuration (config.php)
3. Initialize autoloader (system/engine/autoloader.php)
4. Create Registry (dependency injection container)
5. Load core libraries (config, db, session, cache, etc.)
6. Dispatch startup actions (system/startup/*.php)
7. Route request to controller
8. Execute controller action
9. Render view (Twig template)
10. Send HTTP response
```

#### 3. MVC Flow

```
URL: /product/product&product_id=42
     ↓
Route Parser: Determines controller/action
     ↓
Controller: catalog/controller/product/product.php
     → Load language files
     → Load models (product, category, manufacturer)
     → Fetch data from database
     → Process business logic
     → Prepare data array for view
     ↓
View: catalog/view/template/product/product.twig
     → Render HTML with data
     ↓
Response: HTML page sent to browser
```

### Key Runtime Components

**Registry (Dependency Injection):**
```php
$this->registry->get('db');        // Database connection
$this->registry->get('config');    // Configuration
$this->registry->get('session');   // Session management
$this->registry->get('customer');  // Customer object
$this->registry->get('cart');      // Shopping cart
$this->registry->get('language');  // Translations
$this->registry->get('url');       // URL generator
```

**Loader (Dynamic Loading):**
```php
$this->load->model('catalog/product');     // Load model
$this->load->language('product/product');  // Load translations
$this->load->controller('common/header');  // Load sub-controller
$this->load->view('product/product', $data); // Render template
```

**Event System:**
```php
// Register event
$this->event->register('catalog/model/catalog/product/getProduct/after', 
                       new Action('extension/module/custom/modifyProduct'));

// Trigger automatically when method called
```

---

## Business Flows

### 1. Product Browsing Flow

**User Journey:**
```
1. Home Page → Featured products loaded
2. Click Category → category/category controller
3. Filter/Sort → AJAX or page reload with query params
4. Click Product → product/product controller
5. View Details → Product data loaded from database
```

**Controller Logic** (`catalog/controller/product/product.php`):
```php
public function index() {
    // Get product ID from URL
    $product_id = $this->request->get['product_id'];
    
    // Load model and fetch product
    $this->load->model('catalog/product');
    $product_info = $this->model_catalog_product->getProduct($product_id);
    
    // Check product exists
    if (!$product_info) {
        return new Action('error/not_found');
    }
    
    // Set meta data
    $this->document->setTitle($product_info['meta_title']);
    
    // Fetch related data
    $images = $this->model_catalog_product->getImages($product_id);
    $options = $this->model_catalog_product->getOptions($product_id);
    $discounts = $this->model_catalog_product->getDiscounts($product_id);
    
    // Calculate pricing with tax
    $price = $this->tax->calculate($product_info['price'], 
                                   $product_info['tax_class_id']);
    
    // Prepare data for view
    $data['product_info'] = $product_info;
    $data['images'] = $images;
    $data['price'] = $price;
    
    // Render view
    $this->response->setOutput($this->load->view('product/product', $data));
}
```

**Model Logic** (`catalog/model/catalog/product.php`):
```php
public function getProduct(int $product_id): array {
    $query = $this->db->query("
        SELECT DISTINCT *, pd.name, p.image,
               (SELECT price FROM product_discount 
                WHERE product_id = p.product_id 
                AND quantity = 1 
                ORDER BY priority ASC LIMIT 1) AS discount,
               (SELECT price FROM product_discount 
                WHERE product_id = p.product_id 
                AND special = 1 
                ORDER BY priority ASC LIMIT 1) AS special
        FROM product p
        LEFT JOIN product_description pd 
          ON p.product_id = pd.product_id
        WHERE p.product_id = '" . (int)$product_id . "'
          AND p.status = '1'
          AND pd.language_id = '" . (int)$this->config->get('config_language_id') . "'
    ");
    
    return $query->row; // Returns associative array or empty
}
```

### 2. Shopping Cart Flow

**Add to Cart:**
```
1. Product Page → Click "Add to Cart"
2. AJAX Request → catalog/controller/checkout/cart.add
3. Validate product, quantity, options
4. Add to session cart → system/library/cart/cart.php
5. Return JSON response with cart count
6. Update cart icon in header
```

**Cart Session Structure:**
```php
$this->session->data['cart'] = [
    'cart_id_1' => [
        'product_id' => 42,
        'quantity' => 2,
        'option' => [
            'size' => 'Large',
            'color' => 'Blue'
        ]
    ],
    'cart_id_2' => [
        'product_id' => 55,
        'quantity' => 1,
        'option' => []
    ]
];
```

**Cart Totals Calculation:**
```php
// system/library/cart/cart.php
public function getTotal() {
    $total = 0;
    
    foreach ($this->getProducts() as $product) {
        $total += $product['price'] * $product['quantity'];
    }
    
    return $total;
}

// Extensible via totals (sub-total, shipping, tax, total)
```

### 3. Checkout Flow

**Multi-Step Checkout:**
```
Step 1: Login / Guest Checkout
   ↓
Step 2: Billing Address
   ↓
Step 3: Shipping Address (if different)
   ↓
Step 4: Shipping Method Selection
   ↓
Step 5: Payment Method Selection
   ↓
Step 6: Order Confirmation
   ↓
Step 7: Payment Processing
   ↓
Step 8: Order Complete
```

**Controller Flow:**
```php
// checkout/checkout controller
public function index() {
    // Check cart not empty
    if (!$this->cart->hasProducts()) {
        $this->response->redirect('checkout/cart');
    }
    
    // Require login for customer pricing
    if (!$this->customer->isLogged() && $this->config->get('config_customer_price')) {
        $this->session->data['redirect'] = 'checkout/checkout';
        $this->response->redirect('account/login');
    }
    
    // Load checkout view with steps
    $this->load->view('checkout/checkout', $data);
}

// Each step is loaded via AJAX
public function save() {
    // Validate addresses, shipping, payment
    // Create order in database
    $this->load->model('checkout/order');
    $order_id = $this->model_checkout_order->addOrder($order_data);
    
    // Redirect to payment gateway or success
}
```

### 4. Admin Order Management

**Order List:**
```
1. Admin Dashboard → Sale > Orders
2. Filter orders by status, date, customer
3. View order details
4. Update order status
5. Add order history notes
6. Generate invoice
7. Send email notification
```

**Order Processing:**
```php
// admin/controller/sale/order.php
public function addHistory() {
    $order_id = $this->request->get['order_id'];
    $order_status_id = $this->request->post['order_status_id'];
    $comment = $this->request->post['comment'];
    $notify = $this->request->post['notify'];
    
    // Update order status
    $this->model_sale_order->addHistory($order_id, [
        'order_status_id' => $order_status_id,
        'comment' => $comment,
        'notify' => $notify
    ]);
    
    // Send email if notify enabled
    if ($notify) {
        $this->sendOrderEmail($order_id);
    }
}
```

---

## PHP Execution Model

### MVC Pattern Implementation

**Controller Base Class:**
```php
namespace Opencart\System\Engine;

abstract class Controller {
    protected Registry $registry;
    
    public function __construct(Registry $registry) {
        $this->registry = $registry;
    }
    
    public function __get($key) {
        return $this->registry->get($key);
    }
}
```

**Model Base Class:**
```php
namespace Opencart\System\Engine;

abstract class Model {
    protected Registry $registry;
    
    public function __construct(Registry $registry) {
        $this->registry = $registry;
    }
    
    public function __get($key) {
        return $this->registry->get($key);
    }
}
```

### Database Access Pattern

**Direct SQL Queries:**
```php
// No ORM - direct SQL construction
$query = $this->db->query("
    SELECT * FROM `" . DB_PREFIX . "product` 
    WHERE product_id = '" . (int)$product_id . "'
    AND status = '1'
");

// Access results
$row = $query->row;        // Single row (associative array)
$rows = $query->rows;      // All rows (array of arrays)
$num_rows = $query->num_rows; // Row count
```

**Database Abstraction:**
```php
// Supports multiple databases
class MySQLi {
    public function query($sql) {
        $result = mysqli_query($this->connection, $sql);
        return new Result($result);
    }
    
    public function escape($value) {
        return mysqli_real_escape_string($this->connection, $value);
    }
}
```

### Template Rendering

**Twig Integration:**
```php
// Load and render template
$template = $this->load->view('product/product', $data);

// Twig template: product/product.twig
{{ heading_title }}
{% if product_info.image %}
    <img src="{{ product_info.image }}" alt="{{ heading_title }}"/>
{% endif %}
{{ product_info.description }}
```

**Data Flow:**
```
Controller → $data array → Twig Template → HTML Output
```

### Session Management

**Session Storage:**
```php
// File-based (default)
class File implements SessionHandlerInterface {
    public function write($session_id, $data) {
        file_put_contents(DIR_SESSION . $session_id, $data);
    }
}

// Database-based (optional)
class DB implements SessionHandlerInterface {
    public function write($session_id, $data) {
        $this->db->query("REPLACE INTO session SET ...");
    }
}
```

**Session Usage:**
```php
// Store data
$this->session->data['user_id'] = 123;
$this->session->data['cart'] = ['item1', 'item2'];

// Access data
$user_id = $this->session->data['user_id'];
```

---

## Summary

OpenCart 3.0.7.4 is a mature, feature-rich e-commerce platform built on traditional PHP MVC architecture. Key characteristics:

- **Server-side rendered** with Twig templates
- **Direct SQL** database access (no ORM)
- **Session-based** state management
- **Modular extension system** for payments, shipping, modules
- **Multi-language and multi-store** support
- **Event-driven** extensibility
- **Comprehensive admin panel** for store management

This implementation provides a solid foundation for migration, with clearly separated concerns (MVC), well-defined business logic, and extensive functionality that must be preserved in the target FastAPI + React system.

---

**Next Document**: [02-current-architecture-php-hld-lld.md](./02-current-architecture-php-hld-lld.md) - Detailed architectural analysis
