import React, { Component } from 'react';
import {getEntityData} from './service';
import logo from './img/ezest.png';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.updateURL = this.updateURL.bind(this);
    this.getEntityData = this.getEntityData.bind(this);
    this.state = {
      entityData: [],
      isSearchEnabled: false,
      textData: ''
    }
  }

  updateURL(e) {
    this.setState({ [e.target.name]: e.target.value });
  }

  getEntityData() {
    this.setState({ entityData: [], isSearchEnabled: true });
    getEntityData(this.state.url).then(resp => {
      this.setState({ isSearchEnabled: false });
      if(resp && resp.data && resp.data.entity_list) {
        this.setState({entityData: resp.data.entity_list, textData: resp.data.text });
      }
    }, err=> {
      this.setState({ isSearchEnabled: false });
    });
  }

  render() {
    return (
      <div className="app-container" style={{ height: window.innerHeight }}>
      <div className="app-header">
        <img src={logo} />
        <span>Medical Entity Extractor</span>
      </div>
      <div className="search-container">
        <input type="text" name="url" onChange={this.updateURL} />
        <button onClick={this.getEntityData}>Analyze</button>
      </div>
      {this.state.entityData.length > 0 && (
        <div className="result-container">
          <div className="text-data-container">{this.state.textData}</div>
          <div className="header-container">
            <div className="header">Entity</div>
            <div className="header">Type</div>
            <div className="header cat">Category</div>
          </div>
          <div className="data-container" style={{ height: window.innerHeight - 339, overflow: 'auto'}}>
            {this.state.entityData.map((item, index) => (
              <div key={index} className="wrapper">
                <div className="data">{item.Text}</div>
                <div className="data">{item.Type}</div>
                <div className="data cat">{item.Category}</div>
              </div>
            ))}
          </div>
        </div>
      )}
      {this.state.isSearchEnabled && (
        <div className="loader-container">Loading...</div>
      )}
      </div>
    );
  }
}

export default App;
