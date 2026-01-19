# Current Architecture - PHP OpenCart HLD & LLD

**Document Version**: 1.0  
**Last Updated**: 2025-01-19  
**Purpose**: High-Level and Low-Level architectural analysis of OpenCart 3.0.7.4

---

## Table of Contents

1. [High-Level Architecture (HLD)](#high-level-architecture-hld)
2. [Low-Level Architecture (LLD)](#low-level-architecture-lld)
3. [Module Interactions](#module-interactions)
4. [Data Access Patterns](#data-access-patterns)
5. [Template Rendering Flow](#template-rendering-flow)
6. [Database Schema Overview](#database-schema-overview)

---

## High-Level Architecture (HLD)

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Web Browser (Client)                     │
│  ┌──────────────────┐              ┌──────────────────┐         │
│  │  Customer UI     │              │   Admin Panel    │         │
│  │  (Storefront)    │              │   (Dashboard)    │         │
│  └──────────────────┘              └──────────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                        │                         │
                   HTTP │                         │ HTTP
                        ▼                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Apache/Nginx Web Server                       │
│                    ┌───────────────────┐                        │
│                    │   mod_rewrite /   │                        │
│                    │   URL Routing     │                        │
│                    └───────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     PHP 8.0+ Runtime                            │
│  ┌──────────────────────┐        ┌──────────────────────┐      │
│  │   Catalog App        │        │    Admin App         │      │
│  │   (index.php)        │        │  (admin/index.php)   │      │
│  └──────────────────────┘        └──────────────────────┘      │
│                   │                           │                 │
│                   └───────────┬───────────────┘                 │
│                               ▼                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              OpenCart Framework (MVC)                    │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │  Bootstrap & Routing                             │   │  │
│  │  │  - Registry (DI Container)                       │   │  │
│  │  │  - Action Dispatcher                             │   │  │
│  │  │  - Event System                                  │   │  │
│  │  └──────────────────────────────────────────────────┘   │  │
│  │                                                          │  │
│  │  ┌───────────────┐  ┌───────────────┐  ┌────────────┐  │  │
│  │  │ Controllers   │  │    Models     │  │   Views    │  │  │
│  │  │ (Business     │→ │ (Data Access) │  │  (Twig)    │  │  │
│  │  │  Logic)       │  │               │  │            │  │  │
│  │  └───────────────┘  └───────────────┘  └────────────┘  │  │
│  │          │                  │                           │  │
│  └──────────┼──────────────────┼───────────────────────────┘  │
│             │                  │                              │
│             ▼                  ▼                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │         Core Libraries & Helpers                      │    │
│  │  - Database (MySQLi/PDO)    - Session Management     │    │
│  │  - Cache (File/Redis)       - Language/Translation   │    │
│  │  - Cart Logic               - URL Generator          │    │
│  │  - Customer Object          - Mail System            │    │
│  │  - Image Processor          - Validation Helpers     │    │
│  └──────────────────────────────────────────────────────┘    │
│                               │                              │
└───────────────────────────────┼──────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MySQL/MariaDB Database                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Products │  │Customers │  │  Orders  │  │Extensions│ ...  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    File System Storage                          │
│  - Product Images         - Downloaded Files                    │
│  - Session Files          - Cache Files                         │
│  - Logs                   - Modification Archives               │
└─────────────────────────────────────────────────────────────────┘
```

### Component Overview

#### 1. Presentation Layer

**Catalog (Storefront):**
- Entry Point: `upload/index.php`
- Purpose: Customer-facing e-commerce interface
- Responsibilities:
  - Product browsing and search
  - Shopping cart management
  - Customer account operations
  - Checkout and order placement

**Admin Panel:**
- Entry Point: `upload/admin/index.php`
- Purpose: Store management interface
- Responsibilities:
  - Product and catalog management
  - Order processing
  - Customer management
  - System configuration
  - Extension management

#### 2. Application Layer

**MVC Framework Components:**

**Controllers:**
- Handle HTTP requests
- Execute business logic
- Coordinate between models and views
- Return rendered responses

**Models:**
- Database interaction layer
- Data validation and sanitization
- Business rule implementation
- Query construction and execution

**Views (Twig Templates):**
- HTML rendering
- Data presentation
- Template inheritance
- Partial includes

#### 3. Framework Core

**Registry (Dependency Injection):**
```php
class Registry {
    private array $data = [];
    
    public function set(string $key, $value): void {
        $this->data[$key] = $value;
    }
    
    public function get(string $key) {
        return $this->data[$key] ?? null;
    }
}
```

**Action Dispatcher:**
```php
class Action {
    private string $route;
    
    public function execute(Registry $registry, array &$args = []) {
        // Parse route: 'product/product' -> ProductController::index()
        // Load controller file
        // Instantiate controller
        // Call method with arguments
    }
}
```

**Event System:**
```php
class Event {
    private array $events = [];
    
    public function register(string $trigger, Action $action): void {
        $this->events[$trigger][] = $action;
    }
    
    public function trigger(string $trigger, array &$args = []): void {
        foreach ($this->events[$trigger] as $action) {
            $action->execute($this->registry, $args);
        }
    }
}
```

#### 4. Data Layer

**Database Abstraction:**
- Supports MySQLi, PDO, PostgreSQL
- Direct SQL queries (no ORM)
- Connection pooling and query caching
- Prepared statement support

**Cache Layer:**
- Multiple backends: File, Redis, Memcached, APCu
- Configurable per-store
- Cache invalidation on data changes

#### 5. Extension System

**Extension Architecture:**
```
Extension Package
├── admin/
│   ├── controller/  (Admin config pages)
│   ├── model/       (Admin data operations)
│   └── view/        (Admin templates)
└── catalog/
    ├── controller/  (Frontend functionality)
    ├── model/       (Data access)
    └── view/        (Frontend templates)
```

**Extension Types:**
- **Payment Methods**: Bank transfer, COD, PayPal, Stripe
- **Shipping Methods**: Flat rate, weight-based, free shipping
- **Modules**: Featured products, banners, blog
- **Themes**: UI customization
- **Analytics**: Google Analytics, Facebook Pixel
- **Total Modifiers**: Tax, discount, coupon calculators

---

## Low-Level Architecture (LLD)

### Module Breakdown

#### Catalog Module Structure

**Product Management:**

```php
// Controller: catalog/controller/product/product.php
namespace Opencart\Catalog\Controller\Product;

class Product extends \Opencart\System\Engine\Controller {
    public function index(): void {
        // 1. Validate product_id from request
        $product_id = (int)$this->request->get['product_id'];
        
        // 2. Load product model
        $this->load->model('catalog/product');
        
        // 3. Fetch product data
        $product_info = $this->model_catalog_product->getProduct($product_id);
        
        if (!$product_info) {
            return new Action('error/not_found');
        }
        
        // 4. Load related data
        $images = $this->model_catalog_product->getImages($product_id);
        $options = $this->model_catalog_product->getOptions($product_id);
        $reviews = $this->model_catalog_product->getReviews($product_id);
        
        // 5. Calculate pricing
        $price = $this->tax->calculate(
            $product_info['price'],
            $product_info['tax_class_id']
        );
        
        // 6. Update view count
        $this->model_catalog_product->updateViewed($product_id);
        
        // 7. Prepare view data
        $data['heading_title'] = $product_info['name'];
        $data['product_info'] = $product_info;
        $data['images'] = $images;
        $data['price'] = $this->currency->format($price);
        
        // 8. Render template
        $this->response->setOutput($this->load->view('product/product', $data));
    }
}

// Model: catalog/model/catalog/product.php
namespace Opencart\Catalog\Model\Catalog;

class Product extends \Opencart\System\Engine\Model {
    public function getProduct(int $product_id): array {
        $query = $this->db->query("
            SELECT DISTINCT *,
                   pd.name AS name,
                   pd.description,
                   pd.meta_title,
                   pd.meta_description,
                   m.name AS manufacturer,
                   (SELECT price FROM " . DB_PREFIX . "product_discount pd2
                    WHERE pd2.product_id = p.product_id
                    AND pd2.customer_group_id = '" . (int)$this->config->get('config_customer_group_id') . "'
                    AND pd2.quantity = '1'
                    AND ((pd2.date_start = '0000-00-00' OR pd2.date_start < NOW())
                    AND (pd2.date_end = '0000-00-00' OR pd2.date_end > NOW()))
                    ORDER BY pd2.priority ASC, pd2.price ASC LIMIT 1) AS discount,
                   (SELECT price FROM " . DB_PREFIX . "product_special ps
                    WHERE ps.product_id = p.product_id
                    AND ps.customer_group_id = '" . (int)$this->config->get('config_customer_group_id') . "'
                    AND ((ps.date_start = '0000-00-00' OR ps.date_start < NOW())
                    AND (ps.date_end = '0000-00-00' OR ps.date_end > NOW()))
                    ORDER BY ps.priority ASC, ps.price ASC LIMIT 1) AS special
            FROM " . DB_PREFIX . "product p
            LEFT JOIN " . DB_PREFIX . "product_description pd
                ON (p.product_id = pd.product_id)
            LEFT JOIN " . DB_PREFIX . "manufacturer m
                ON (p.manufacturer_id = m.manufacturer_id)
            WHERE p.product_id = '" . (int)$product_id . "'
            AND p.status = '1'
            AND p.date_available <= NOW()
            AND pd.language_id = '" . (int)$this->config->get('config_language_id') . "'
        ");
        
        return $query->row;
    }
    
    public function getImages(int $product_id): array {
        $query = $this->db->query("
            SELECT * FROM " . DB_PREFIX . "product_image
            WHERE product_id = '" . (int)$product_id . "'
            ORDER BY sort_order ASC
        ");
        
        return $query->rows;
    }
}
```

#### Cart Module Structure

**Cart Library:**

```php
// system/library/cart/cart.php
namespace Opencart\System\Library\Cart;

class Cart {
    private Registry $registry;
    private array $data = [];
    
    public function __construct(Registry $registry) {
        $this->registry = $registry;
        
        // Load cart from session
        if (isset($this->session->data['cart'])) {
            $this->data = $this->session->data['cart'];
        }
    }
    
    public function add(int $product_id, int $quantity = 1, array $option = []): void {
        // Generate cart key
        $key = $this->generateKey($product_id, $option);
        
        // Check if product exists
        if (isset($this->data[$key])) {
            $this->data[$key]['quantity'] += $quantity;
        } else {
            $this->data[$key] = [
                'product_id' => $product_id,
                'quantity' => $quantity,
                'option' => $option
            ];
        }
        
        // Save to session
        $this->session->data['cart'] = $this->data;
    }
    
    public function remove(string $key): void {
        if (isset($this->data[$key])) {
            unset($this->data[$key]);
            $this->session->data['cart'] = $this->data;
        }
    }
    
    public function getProducts(): array {
        $products = [];
        
        foreach ($this->data as $key => $cart_item) {
            $product_id = $cart_item['product_id'];
            
            // Load product model
            $this->load->model('catalog/product');
            $product_info = $this->model_catalog_product->getProduct($product_id);
            
            if ($product_info) {
                // Calculate price with options
                $price = $product_info['price'];
                
                foreach ($cart_item['option'] as $product_option_id => $value) {
                    $option_info = $this->model_catalog_product->getOption($product_id, $product_option_id);
                    
                    if ($option_info['type'] == 'select' || $option_info['type'] == 'radio') {
                        $option_value_info = $this->model_catalog_product->getOptionValue($product_id, $value);
                        
                        if ($option_value_info['price_prefix'] == '+') {
                            $price += $option_value_info['price'];
                        } elseif ($option_value_info['price_prefix'] == '-') {
                            $price -= $option_value_info['price'];
                        }
                    }
                }
                
                $products[$key] = [
                    'cart_id' => $key,
                    'product_id' => $product_id,
                    'name' => $product_info['name'],
                    'model' => $product_info['model'],
                    'image' => $product_info['image'],
                    'option' => $cart_item['option'],
                    'quantity' => $cart_item['quantity'],
                    'price' => $price,
                    'total' => $price * $cart_item['quantity']
                ];
            }
        }
        
        return $products;
    }
    
    public function getTotal(): float {
        $total = 0;
        
        foreach ($this->getProducts() as $product) {
            $total += $product['total'];
        }
        
        return $total;
    }
    
    private function generateKey(int $product_id, array $option): string {
        return base64_encode(serialize([$product_id, $option]));
    }
}
```

#### Checkout Module Structure

**Checkout Flow:**

```php
// catalog/controller/checkout/checkout.php
namespace Opencart\Catalog\Controller\Checkout;

class Checkout extends \Opencart\System\Engine\Controller {
    public function index(): void {
        // 1. Validate cart not empty
        if (!$this->cart->hasProducts()) {
            $this->response->redirect('checkout/cart');
            return;
        }
        
        // 2. Check customer logged in (if required)
        if (!$this->customer->isLogged() && $this->config->get('config_customer_price')) {
            $this->session->data['redirect'] = 'checkout/checkout';
            $this->response->redirect('account/login');
            return;
        }
        
        // 3. Load checkout template with AJAX steps
        $data['logged'] = $this->customer->isLogged();
        $data['shipping_required'] = $this->cart->hasShipping();
        
        // 4. Render multi-step checkout page
        $this->response->setOutput($this->load->view('checkout/checkout', $data));
    }
    
    // AJAX: Save payment address
    public function savePaymentAddress(): void {
        $json = [];
        
        // Validate input
        if (!$this->request->post['firstname']) {
            $json['error']['firstname'] = 'First name required';
        }
        
        if (!$json) {
            // Save to session
            $this->session->data['payment_address'] = $this->request->post;
            
            // Load payment methods
            $this->load->model('checkout/payment_method');
            $payment_methods = $this->model_checkout_payment_method->getMethods($this->session->data['payment_address']);
            
            $json['payment_methods'] = $payment_methods;
        }
        
        $this->response->addHeader('Content-Type: application/json');
        $this->response->setOutput(json_encode($json));
    }
    
    // AJAX: Confirm order
    public function confirm(): void {
        $json = [];
        
        // Validate all required data present
        if (!isset($this->session->data['payment_address'])) {
            $json['error'] = 'Payment address required';
        }
        
        if (!isset($this->session->data['payment_method'])) {
            $json['error'] = 'Payment method required';
        }
        
        if (!$json) {
            // Prepare order data
            $order_data = [];
            
            $order_data['payment_firstname'] = $this->session->data['payment_address']['firstname'];
            $order_data['payment_lastname'] = $this->session->data['payment_address']['lastname'];
            $order_data['payment_address_1'] = $this->session->data['payment_address']['address_1'];
            $order_data['payment_city'] = $this->session->data['payment_address']['city'];
            $order_data['payment_postcode'] = $this->session->data['payment_address']['postcode'];
            $order_data['payment_country'] = $this->session->data['payment_address']['country'];
            $order_data['payment_method'] = $this->session->data['payment_method'];
            
            // Add shipping if required
            if ($this->cart->hasShipping()) {
                $order_data['shipping_firstname'] = $this->session->data['shipping_address']['firstname'];
                $order_data['shipping_method'] = $this->session->data['shipping_method'];
            }
            
            // Add products
            $order_data['products'] = [];
            foreach ($this->cart->getProducts() as $product) {
                $order_data['products'][] = [
                    'product_id' => $product['product_id'],
                    'name' => $product['name'],
                    'model' => $product['model'],
                    'quantity' => $product['quantity'],
                    'price' => $product['price'],
                    'total' => $product['total']
                ];
            }
            
            // Calculate totals
            $order_data['totals'] = $this->calculateTotals();
            
            // Create order
            $this->load->model('checkout/order');
            $order_id = $this->model_checkout_order->addOrder($order_data);
            
            $json['order_id'] = $order_id;
            $json['success'] = 'Order placed successfully';
            
            // Clear cart
            $this->cart->clear();
        }
        
        $this->response->addHeader('Content-Type: application/json');
        $this->response->setOutput(json_encode($json));
    }
    
    private function calculateTotals(): array {
        $totals = [];
        $total = 0;
        $taxes = $this->cart->getTaxes();
        
        // Sub-total
        $totals[] = [
            'code' => 'sub_total',
            'title' => 'Sub-Total',
            'value' => $this->cart->getSubTotal(),
            'sort_order' => 1
        ];
        $total += $this->cart->getSubTotal();
        
        // Shipping
        if ($this->cart->hasShipping()) {
            $shipping_cost = $this->session->data['shipping_method']['cost'];
            $totals[] = [
                'code' => 'shipping',
                'title' => $this->session->data['shipping_method']['title'],
                'value' => $shipping_cost,
                'sort_order' => 3
            ];
            $total += $shipping_cost;
        }
        
        // Tax
        foreach ($taxes as $tax_id => $value) {
            $totals[] = [
                'code' => 'tax',
                'title' => $this->tax->getRateName($tax_id),
                'value' => $value,
                'sort_order' => 5
            ];
            $total += $value;
        }
        
        // Total
        $totals[] = [
            'code' => 'total',
            'title' => 'Total',
            'value' => $total,
            'sort_order' => 9
        ];
        
        return $totals;
    }
}
```

#### Admin Order Management

```php
// admin/controller/sale/order.php
namespace Opencart\Admin\Controller\Sale;

class Order extends \Opencart\System\Engine\Controller {
    public function index(): void {
        $this->load->language('sale/order');
        
        // Set page title
        $this->document->setTitle($this->language->get('heading_title'));
        
        // Load model
        $this->load->model('sale/order');
        
        // Get orders with filters
        $filter_data = [
            'filter_order_id' => $this->request->get['filter_order_id'] ?? null,
            'filter_customer' => $this->request->get['filter_customer'] ?? null,
            'filter_order_status_id' => $this->request->get['filter_order_status_id'] ?? null,
            'filter_date_from' => $this->request->get['filter_date_from'] ?? null,
            'filter_date_to' => $this->request->get['filter_date_to'] ?? null,
            'start' => ($this->request->get['page'] ?? 1 - 1) * $this->config->get('config_pagination'),
            'limit' => $this->config->get('config_pagination')
        ];
        
        $orders = $this->model_sale_order->getOrders($filter_data);
        $order_total = $this->model_sale_order->getTotalOrders($filter_data);
        
        // Prepare view data
        $data['orders'] = [];
        
        foreach ($orders as $order) {
            $data['orders'][] = [
                'order_id' => $order['order_id'],
                'customer' => $order['customer'],
                'status' => $order['order_status'],
                'total' => $this->currency->format($order['total'], $order['currency_code']),
                'date_added' => date($this->language->get('date_format_short'), strtotime($order['date_added'])),
                'edit' => $this->url->link('sale/order.info', 'order_id=' . $order['order_id'])
            ];
        }
        
        // Pagination
        $data['pagination'] = $this->load->controller('common/pagination', [
            'total' => $order_total,
            'page' => $this->request->get['page'] ?? 1,
            'limit' => $this->config->get('config_pagination'),
            'url' => $this->url->link('sale/order')
        ]);
        
        $this->response->setOutput($this->load->view('sale/order_list', $data));
    }
    
    public function info(): void {
        $order_id = $this->request->get['order_id'];
        
        $this->load->model('sale/order');
        $order_info = $this->model_sale_order->getOrder($order_id);
        
        if (!$order_info) {
            return new Action('error/not_found');
        }
        
        // Load order products
        $data['products'] = $this->model_sale_order->getProducts($order_id);
        
        // Load order totals
        $data['totals'] = $this->model_sale_order->getTotals($order_id);
        
        // Load order history
        $data['histories'] = $this->model_sale_order->getHistories($order_id);
        
        // Load order statuses for update
        $this->load->model('localisation/order_status');
        $data['order_statuses'] = $this->model_localisation_order_status->getOrderStatuses();
        
        $this->response->setOutput($this->load->view('sale/order_info', $data));
    }
    
    public function addHistory(): void {
        $json = [];
        
        if (!$this->user->hasPermission('modify', 'sale/order')) {
            $json['error'] = 'Permission denied';
        }
        
        if (!$json) {
            $order_id = $this->request->get['order_id'];
            
            $this->load->model('sale/order');
            $this->model_sale_order->addHistory($order_id, [
                'order_status_id' => $this->request->post['order_status_id'],
                'notify' => $this->request->post['notify'] ?? false,
                'comment' => $this->request->post['comment'] ?? ''
            ]);
            
            $json['success'] = 'Order history added';
            
            // Send email notification if requested
            if ($this->request->post['notify']) {
                $this->sendOrderStatusEmail($order_id);
            }
        }
        
        $this->response->addHeader('Content-Type: application/json');
        $this->response->setOutput(json_encode($json));
    }
}
```

---

## Module Interactions

### Request Flow Diagram

```
HTTP Request → index.php
    ↓
Bootstrap (startup actions)
    ↓
Route Parsing
    ↓
Controller Loading
    ↓
┌────────────────────────────────────────┐
│         Controller Actions             │
│  1. Load language files                │
│  2. Load models                        │
│  3. Execute business logic             │
│  4. Prepare data for view              │
│  5. Load sub-controllers (header, etc.)│
└────────────────────────────────────────┘
    ↓                    ↓
Model Layer         View Layer
    ↓                    ↓
Database Query      Twig Render
    ↓                    ↓
Results            HTML Output
    ↓                    ↓
    └──────────┬─────────┘
               ↓
         HTTP Response
```

### Module Communication

**Controller → Model:**
```php
// Controller loads model via Loader
$this->load->model('catalog/product');

// Access model via Registry
$product_info = $this->model_catalog_product->getProduct($product_id);
```

**Controller → View:**
```php
// Prepare data array
$data['heading_title'] = 'Product Page';
$data['product_info'] = $product_info;

// Load view (Twig template)
$output = $this->load->view('product/product', $data);

// Set response
$this->response->setOutput($output);
```

**Controller → Controller (Sub-controllers):**
```php
// Load common components
$data['header'] = $this->load->controller('common/header');
$data['footer'] = $this->load->controller('common/footer');
```

**Event Triggers:**
```php
// Before method call
$this->event->trigger('catalog/model/catalog/product/getProduct/before', [&$product_id]);

// After method call
$this->event->trigger('catalog/model/catalog/product/getProduct/after', [&$product_id, &$product_info]);
```

---

## Data Access Patterns

### Database Query Patterns

**Direct SQL Construction:**
```php
public function getProducts(array $filter = []): array {
    $sql = "SELECT * FROM " . DB_PREFIX . "product p";
    $sql .= " LEFT JOIN " . DB_PREFIX . "product_description pd ON p.product_id = pd.product_id";
    
    $sql .= " WHERE pd.language_id = '" . (int)$this->config->get('config_language_id') . "'";
    $sql .= " AND p.status = '1'";
    
    if (!empty($filter['filter_name'])) {
        $sql .= " AND pd.name LIKE '%" . $this->db->escape($filter['filter_name']) . "%'";
    }
    
    if (!empty($filter['filter_category_id'])) {
        $sql .= " AND p.product_id IN (SELECT product_id FROM " . DB_PREFIX . "product_to_category WHERE category_id = '" . (int)$filter['filter_category_id'] . "')";
    }
    
    $sort_data = [
        'pd.name',
        'p.model',
        'p.price',
        'p.sort_order'
    ];
    
    if (isset($filter['sort']) && in_array($filter['sort'], $sort_data)) {
        $sql .= " ORDER BY " . $filter['sort'];
    } else {
        $sql .= " ORDER BY p.sort_order";
    }
    
    $sql .= " " . ($filter['order'] == 'DESC' ? 'DESC' : 'ASC');
    
    if (isset($filter['start']) && isset($filter['limit'])) {
        $sql .= " LIMIT " . (int)$filter['start'] . "," . (int)$filter['limit'];
    }
    
    $query = $this->db->query($sql);
    
    return $query->rows;
}
```

**Transaction Support:**
```php
public function addOrder(array $order_data): int {
    $this->db->query("START TRANSACTION");
    
    try {
        // Insert order
        $this->db->query("INSERT INTO `" . DB_PREFIX . "order` SET ...");
        $order_id = $this->db->getLastId();
        
        // Insert order products
        foreach ($order_data['products'] as $product) {
            $this->db->query("INSERT INTO `" . DB_PREFIX . "order_product` SET order_id = '" . (int)$order_id . "', ...");
        }
        
        // Insert order totals
        foreach ($order_data['totals'] as $total) {
            $this->db->query("INSERT INTO `" . DB_PREFIX . "order_total` SET order_id = '" . (int)$order_id . "', ...");
        }
        
        $this->db->query("COMMIT");
        
        return $order_id;
    } catch (Exception $e) {
        $this->db->query("ROLLBACK");
        throw $e;
    }
}
```

### Caching Strategy

**Model-Level Caching:**
```php
public function getProduct(int $product_id): array {
    $cache_key = 'product.' . (int)$product_id;
    
    $product_info = $this->cache->get($cache_key);
    
    if (!$product_info) {
        $query = $this->db->query("SELECT * FROM ...");
        $product_info = $query->row;
        
        $this->cache->set($cache_key, $product_info);
    }
    
    return $product_info;
}
```

**Cache Invalidation:**
```php
public function editProduct(int $product_id, array $data): void {
    // Update database
    $this->db->query("UPDATE " . DB_PREFIX . "product SET ...");
    
    // Invalidate cache
    $this->cache->delete('product.' . (int)$product_id);
}
```

---

## Template Rendering Flow

### Twig Integration

**Template Loading:**
```php
// system/library/template/twig.php
public function render(string $filename, array $data = []): string {
    $loader = new \Twig\Loader\FilesystemLoader(DIR_TEMPLATE);
    $twig = new \Twig\Environment($loader, [
        'cache' => DIR_CACHE . 'template/',
        'auto_reload' => true
    ]);
    
    // Add custom filters
    $twig->addFilter(new \Twig\TwigFilter('currency', [$this, 'currencyFilter']));
    $twig->addFilter(new \Twig\TwigFilter('date_format', [$this, 'dateFilter']));
    
    // Render template
    return $twig->render($filename, $data);
}
```

**Template Structure:**
```twig
{# product/product.twig #}
{{ header }}

<div id="product-product">
    <div class="row">
        <div class="col-sm-6">
            {% if product_info.image %}
                <img src="{{ product_info.image }}" alt="{{ heading_title }}" class="img-responsive"/>
            {% endif %}
            
            {% if images %}
                <div class="thumbnails">
                    {% for image in images %}
                        <img src="{{ image.thumb }}" alt="" class="img-thumbnail"/>
                    {% endfor %}
                </div>
            {% endif %}
        </div>
        
        <div class="col-sm-6">
            <h1>{{ heading_title }}</h1>
            
            {% if price %}
                <ul class="list-unstyled">
                    {% if not special %}
                        <li><h2>{{ price }}</h2></li>
                    {% else %}
                        <li><span style="text-decoration: line-through;">{{ price }}</span></li>
                        <li><h2>{{ special }}</h2></li>
                    {% endif %}
                </ul>
            {% endif %}
            
            <div id="product">
                {% if options %}
                    {% for option in options %}
                        <div class="form-group{% if option.required %} required {% endif %}">
                            <label class="control-label">{{ option.name }}</label>
                            <select name="option[{{ option.product_option_id }}]" class="form-control">
                                <option value="">{{ text_select }}</option>
                                {% for option_value in option.product_option_value %}
                                    <option value="{{ option_value.product_option_value_id }}">
                                        {{ option_value.name }}
                                        {% if option_value.price %}
                                            ({{ option_value.price_prefix }}{{ option_value.price }})
                                        {% endif %}
                                    </option>
                                {% endfor %}
                            </select>
                        </div>
                    {% endfor %}
                {% endif %}
                
                <div class="form-group">
                    <label class="control-label" for="input-quantity">{{ entry_qty }}</label>
                    <input type="text" name="quantity" value="{{ minimum }}" id="input-quantity" class="form-control"/>
                    <button type="button" id="button-cart" class="btn btn-primary btn-lg btn-block">{{ button_cart }}</button>
                </div>
            </div>
            
            {{ product_info.description }}
        </div>
    </div>
</div>

{{ footer }}
```

---

## Database Schema Overview

### Core Tables

**Product Tables:**
```sql
-- Product main table
CREATE TABLE `oc_product` (
    `product_id` int(11) NOT NULL AUTO_INCREMENT,
    `model` varchar(64) NOT NULL,
    `sku` varchar(64) NOT NULL,
    `upc` varchar(12) NOT NULL,
    `ean` varchar(14) NOT NULL,
    `jan` varchar(13) NOT NULL,
    `isbn` varchar(17) NOT NULL,
    `mpn` varchar(64) NOT NULL,
    `location` varchar(128) NOT NULL,
    `quantity` int(4) NOT NULL DEFAULT '0',
    `stock_status_id` int(11) NOT NULL,
    `image` varchar(255) DEFAULT NULL,
    `manufacturer_id` int(11) NOT NULL,
    `shipping` tinyint(1) NOT NULL DEFAULT '1',
    `price` decimal(15,4) NOT NULL DEFAULT '0.0000',
    `points` int(8) NOT NULL DEFAULT '0',
    `tax_class_id` int(11) NOT NULL,
    `date_available` date NOT NULL DEFAULT '0000-00-00',
    `weight` decimal(15,8) NOT NULL DEFAULT '0.00000000',
    `weight_class_id` int(11) NOT NULL DEFAULT '0',
    `length` decimal(15,8) NOT NULL DEFAULT '0.00000000',
    `width` decimal(15,8) NOT NULL DEFAULT '0.00000000',
    `height` decimal(15,8) NOT NULL DEFAULT '0.00000000',
    `length_class_id` int(11) NOT NULL DEFAULT '0',
    `subtract` tinyint(1) NOT NULL DEFAULT '1',
    `minimum` int(11) NOT NULL DEFAULT '1',
    `sort_order` int(11) NOT NULL DEFAULT '0',
    `status` tinyint(1) NOT NULL DEFAULT '0',
    `viewed` int(5) NOT NULL DEFAULT '0',
    `date_added` datetime NOT NULL,
    `date_modified` datetime NOT NULL,
    PRIMARY KEY (`product_id`)
);

-- Product descriptions (multi-language)
CREATE TABLE `oc_product_description` (
    `product_id` int(11) NOT NULL,
    `language_id` int(11) NOT NULL,
    `name` varchar(255) NOT NULL,
    `description` text NOT NULL,
    `tag` text NOT NULL,
    `meta_title` varchar(255) NOT NULL,
    `meta_description` varchar(255) NOT NULL,
    `meta_keyword` varchar(255) NOT NULL,
    PRIMARY KEY (`product_id`,`language_id`)
);

-- Product to category mapping
CREATE TABLE `oc_product_to_category` (
    `product_id` int(11) NOT NULL,
    `category_id` int(11) NOT NULL,
    PRIMARY KEY (`product_id`,`category_id`)
);
```

**Customer Tables:**
```sql
CREATE TABLE `oc_customer` (
    `customer_id` int(11) NOT NULL AUTO_INCREMENT,
    `customer_group_id` int(11) NOT NULL,
    `store_id` int(11) NOT NULL DEFAULT '0',
    `language_id` int(11) NOT NULL,
    `firstname` varchar(32) NOT NULL,
    `lastname` varchar(32) NOT NULL,
    `email` varchar(96) NOT NULL,
    `telephone` varchar(32) NOT NULL,
    `password` varchar(255) NOT NULL,
    `salt` varchar(9) NOT NULL,
    `newsletter` tinyint(1) NOT NULL DEFAULT '0',
    `status` tinyint(1) NOT NULL,
    `approved` tinyint(1) NOT NULL,
    `safe` tinyint(1) NOT NULL,
    `token` text NOT NULL,
    `ip` varchar(40) NOT NULL,
    `date_added` datetime NOT NULL,
    PRIMARY KEY (`customer_id`)
);

CREATE TABLE `oc_address` (
    `address_id` int(11) NOT NULL AUTO_INCREMENT,
    `customer_id` int(11) NOT NULL,
    `firstname` varchar(32) NOT NULL,
    `lastname` varchar(32) NOT NULL,
    `company` varchar(60) NOT NULL,
    `address_1` varchar(128) NOT NULL,
    `address_2` varchar(128) NOT NULL,
    `city` varchar(128) NOT NULL,
    `postcode` varchar(10) NOT NULL,
    `country_id` int(11) NOT NULL DEFAULT '0',
    `zone_id` int(11) NOT NULL DEFAULT '0',
    `default` tinyint(1) NOT NULL,
    PRIMARY KEY (`address_id`)
);
```

**Order Tables:**
```sql
CREATE TABLE `oc_order` (
    `order_id` int(11) NOT NULL AUTO_INCREMENT,
    `invoice_no` int(11) NOT NULL DEFAULT '0',
    `invoice_prefix` varchar(26) NOT NULL,
    `store_id` int(11) NOT NULL DEFAULT '0',
    `store_name` varchar(64) NOT NULL,
    `store_url` varchar(255) NOT NULL,
    `customer_id` int(11) NOT NULL,
    `customer_group_id` int(11) NOT NULL DEFAULT '0',
    `firstname` varchar(32) NOT NULL,
    `lastname` varchar(32) NOT NULL,
    `email` varchar(96) NOT NULL,
    `telephone` varchar(32) NOT NULL,
    `payment_firstname` varchar(32) NOT NULL,
    `payment_lastname` varchar(32) NOT NULL,
    `payment_address_1` varchar(128) NOT NULL,
    `payment_city` varchar(128) NOT NULL,
    `payment_postcode` varchar(10) NOT NULL,
    `payment_country` varchar(128) NOT NULL,
    `payment_method` varchar(128) NOT NULL,
    `shipping_firstname` varchar(32) NOT NULL,
    `shipping_method` varchar(128) NOT NULL,
    `order_status_id` int(11) NOT NULL DEFAULT '0',
    `currency_code` varchar(3) NOT NULL,
    `currency_value` decimal(15,8) NOT NULL DEFAULT '1.00000000',
    `total` decimal(15,4) NOT NULL DEFAULT '0.0000',
    `date_added` datetime NOT NULL,
    `date_modified` datetime NOT NULL,
    PRIMARY KEY (`order_id`)
);

CREATE TABLE `oc_order_product` (
    `order_product_id` int(11) NOT NULL AUTO_INCREMENT,
    `order_id` int(11) NOT NULL,
    `product_id` int(11) NOT NULL,
    `name` varchar(255) NOT NULL,
    `model` varchar(64) NOT NULL,
    `quantity` int(4) NOT NULL,
    `price` decimal(15,4) NOT NULL DEFAULT '0.0000',
    `total` decimal(15,4) NOT NULL DEFAULT '0.0000',
    `tax` decimal(15,4) NOT NULL DEFAULT '0.0000',
    PRIMARY KEY (`order_product_id`)
);
```

---

## Summary

OpenCart's architecture is characterized by:

1. **Traditional MVC Pattern**: Clear separation between controllers (business logic), models (data access), and views (presentation)

2. **Direct Database Access**: SQL queries constructed directly in models without ORM abstraction

3. **Session-Based State**: Cart and user state managed via PHP sessions

4. **Server-Side Rendering**: Twig templates generate complete HTML on the server

5. **Event-Driven Extensibility**: Hook system allows extensions to modify core behavior

6. **Registry Pattern**: Centralized dependency injection container for core services

This architecture provides a solid foundation for migration, with well-defined responsibilities that can be mapped to modern API-first architecture with FastAPI backend and React frontend.

---

**Next Document**: [03-migration-goals-and-modules.md](./03-migration-goals-and-modules.md)
