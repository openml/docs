# React App

### App structure
The structure of the source code looks as follows

App.js  
index.js  
|-- components  
    |-- Sidebar.js  
    |-- Header.js  
    |-- ...  
|-- layouts  
    |-- Clear.js  
    |-- Main.js  
|-- pages  
    |-- auth  
    |-- cover  
    |-- docs  
    |-- search  
|-- routes  
    |-- index.js  
    |-- Routes.js  
|-- themes  

The whole website is designed as a single-page application.
The top level files bootstrap the app. `index.js` simply renders the top component, and
`App.js` adds global state using the React Context API. This includes the current theme, user
authentication, search keywords, and other user input.

`Routes.js` loads the correct components based on the current route (URL). The list of
possible routes is defined in `routes/index.js`.

There are two top level layouts: `Main` loads the main layout with a `Sidebar`, `Header`,
and a certain page. The specific pages are in the `pages` folder. The `Clear.js` layout has no
headers or sidebars, it is used mainly for user login and registration. Finally, `themes` contains the overall theme styling for the entire website.

### Styling
To keep a consistent style and minimize dependencies and complexity, we build on [Material UI](https://material-ui.com/) components and [FontAwesome](https://fontawesome.com) icons. Theming is defined in `themes/index.js` and loaded in as a contect (`ThemeContext`) in `App.js`. More specific styling
is always defined through styled components in the corresponding pages.


### Handling state
There are different levels of state management:  
* Global state is handled via React's native Context API (we don't use Redux). Contexts are defined in the component tree where needed (usually higher up) by a context provider component, and is accessed lower in the component tree by a context consumer. For instance, see the `ThemeContext.Provider` in `App.js` and the `ThemeContext.Consumer` in `Sidebar.js`.  
* Lower level components can pass state to their child components via props.  
* Local state changes should, when possible, be defined by React Hooks.  

#### Lifecycle Methods
These are the React lifecycle methods and how we use them. When a component mounts, methods 1,2,4,7 will be called. When it updates, methods 2-6 will be called.  

1. constructor(): Set the initial state of the components
2. getDerivedStateFromProps(props, state): Static method, only for changing the local state based on props. It returns the new state.
3. shouldComponentUpdate(nextProps, nextState): Decides whether a state change requires a re-rendering or not. Used to optimize performance.
4. render(): Returns the JSX to be rendered. It should NOT change the state.
5. getSnapshotBeforeUpdate(prevProps,prevState): Used to save 'old' DOM information right before an update. Returns a 'snapshot'.
6. componentDidUpdate(prevProps,prevState,snapshot): For async requests or other operations right after component update.
7. componentDidMount(): For async requests (e.g. API calls) right after the component mounted.
8. componentWillUnMount(): Cleanup before the component is destroyed.
9. componentDidCatch(error,info): For updating the state after an error is thrown.

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
