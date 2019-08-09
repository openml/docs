### React components

### Handling state
We manage state through React Hooks. See below for further details.
Authentication information in stored in the `AuthProvider` component.

### Styling
To keep a consistent style and minimize dependencies and complexity, we build on [Material UI](https://material-ui.com/). Overall theming is defined in the parent component `openml.jsx`. Additional styling is defined in the subcomponents themselves.

### React Basics
Here are a few React basics you need to know about when developing the frontend. If you've developed with React before, this will just jog your memory. If you are completely new to React, we recommend 'The Road to learn React' by Robin Wieruch.

#### Components
React only builds the 'View' layer of a web application, depending on APIs to receive information from a backend. The view is a hierarchy of composable _components_, each isolating all the code for rendering a specific part ('box') of the user interface. This is encapsulated in the `render()` method, which renders the component every time something changes. This method returns JSX syntax, a mix of HTML and javascript that allows easy templating. The curly braces {} tell the JSX parser that it needs to interpret the contents. JSX supports most HTML attributes, although some are renamed. For instance, `className` replaces the standard HTML `class` attribute.

Components are usually defined as subclasses of React.Component. Here we define a simple 'App' component:
``` javascript
class App extends Component {
  render() {
    const title = "Welcome to OpenML";
    return (
    <div className="App">
      <h1>{title}</h1>
    </div>
    );
  }
}
```

Components can have multiple child components, which are instantiated inside the parent's render method:
Here's a simple example:
``` javascript
class App extends Component {
  render() {
    return (
    // This instantiates a component of class TitleBar
    <TitleBar />
    <MainComponent />
    );
  }
}
```

We can replace any HTML element with a React component (and all its children). Often, we will simply replace the whole HTML root:
``` javascript
ReactDOM.render(
  <App />,
  document.getElementById('root')
);
```

#### Component state
React components have internal properties and state that can be accessed though the `props` and `state` data structures. `state` stores the data that you need to render the component. It is mutable (via `setState()`) and can be changed asynchronously. It holds anything that can be changed by the component itself. It should not be accessed by child or parent components (consider it private). `props` contains your component's fixed properties (configuration). It is immutable by the component itself, only by its parent. It is used to pass data (and event handlers) from a parent component to a child component. Every time that `props` or `state` change, the component will re-render.

Here is an example of a simple component that changes its own state through a button click.
``` javascript
const titles: {mainTitle: 'OpenML'};

class App extends Component {
  constructor(props){
    super(props); // required
  }
  // State initialization
  // Shorthand for this.state = {titles: titles};
  this.state = {titles};

  // Methods need to be bound to the class to have access to `this`.
  // Arrow functions are automatically bound
  changeMainTitle = (name) => {
    this.setState({titles.mainTitle : name});
  }

  render(){
    return (
      <div classname="App">
        <h1>{this.state.titles.mainTitle}</h1>
        <button type="button"
          //Arrow function passed to onClick event handler
          onClick={() => this.changeMainTitle("NewOpenML")}
          > Update
        </button>
      </div>
    );
  }
}
```

Here is an example of component state being passed on to child components via properties.
Optionally, the `children` prop can be used to pass elements to child components, such as a text string here.
``` javascript
class App extends Component {
  ...
  render(){
    return (
      <div classname="App">
        // Creates a new TitleBar component with a property `title`
        <TitleBar
          title={this.state.titles.mainTitle}
        > Subtext
        </TitleBar>
        <Content />
      </div>
    );
  }
}
class TitleBar extends Component {
  render(){
    // Unpacking (deconstructing) the properties
    const {myTitle, children} = this.props;
    return (
      <h1>{myTitle}</h1>
      {children}
    );
  }
}
```



#### Forms and Events
React wraps native browser events into _synthetic events_ to handle interactions in a cross-browser compatible way. After being wrapped, they are sent to
all event handlers, usually defined as callbacks. Note: for performance reasons, synthetic events are pooled and reused, so their properties are nullified after being consumed. If you want to use them asynchronously, you need to call `event.persist()`.

HTML forms are different than other DOM elements because they keep their own state in plain HTML. To make sure that we can control the state
we need to set the input field's `value` to a component state value.

Here's an example of using an input field to change the title displayed in the component.
``` javascript
const titles: {mainTitle: 'OpenML'};

class App extends Component {
  this.state = {titles};

  // Receive synthetic event
  onTitleChange = (event) => {
    this.setState({titles.mainTitle : event.target.value});
  }

  render(){
    return (      
      <div classname="App">
        <h1>{this.state.titles.mainTitle}</h1>
        <form>
          <input type="text"
          value={this.state.titles.mainTitle} // control state
          onChange={this.onTitleChange} // event handler callback
          />
        </form>
      </div>
    );
  }
}
```

#### Component declarations
