---
icon: material/api
---

# OpenML APIs

OpenML provides APIs for multiple programming languages and use cases. Choose your preferred client library to get started.

## Client Libraries

<div class="grid-cards">

<div class="card">
<h3>Python</h3>
<p>The OpenML Python API provides a convenient way to interact with OpenML from Python. It integrates with scikit-learn and other popular libraries.</p>
<p><a href="python/">Python Documentation →</a></p>
</div>

<div class="card">
<h3>R</h3>
<p>The R client provides a native interface for R users, integrating with popular R machine learning libraries.</p>
<p><a href="r/">R Documentation →</a></p>
</div>

<div class="card">
<h3>Java</h3>
<p>The Java client allows you to integrate OpenML into Java applications.</p>
<p><a href="ecosystem/Java/">Java Documentation →</a></p>
</div>

<div class="card">
<h3>REST API</h3>
<p>The REST API provides direct HTTP access to OpenML services. Use it from any programming language or tool.</p>
<p><a href="ecosystem/Rest/">REST API Documentation →</a></p>
</div>

</div>

## Additional Clients

<div class="grid-cards">

<div class="card">
<h3>PyTorch</h3>
<p>OpenML integration for PyTorch workflows.</p>
<p><a href="pytorch/">PyTorch Documentation →</a></p>
</div>

<div class="card">
<h3>TensorFlow</h3>
<p>OpenML integration for TensorFlow workflows.</p>
<p><a href="tensorflow/">TensorFlow Documentation →</a></p>
</div>

<div class="card">
<h3>Julia</h3>
<p>OpenML.jl - Julia client for OpenML.</p>
<p><a href="julia/">Julia Documentation →</a></p>
</div>

<div class="card">
<h3>APIv2</h3>
<p>The next generation OpenML API.</p>
<p><a href="apiv2/">APIv2 Documentation →</a></p>
</div>

</div>

## Getting Started

### Authentication

To upload data or share experiments, you'll need an OpenML account and API key:

1. [Create an account](https://www.openml.org/auth/sign-up) on OpenML.org
2. Go to your profile page to find your API key
3. Configure your client with the API key

### Testing

For development and testing, use the test server instead of the production server:

- **Test server URL**: https://test.openml.org/
- **Production server URL**: https://www.openml.org/

!!! note "Test Server"
    The test server allows you to experiment without affecting production data. Use it for testing uploads, runs, and other operations.
