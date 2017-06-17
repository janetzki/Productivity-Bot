import { combineReducers } from 'redux'

import bioprotocol from './bioprotocol'
import biochip from './biochip'
import pareto from './pareto'
import text from './text'

const mainReducer = combineReducers({
  bioprotocol: bioprotocol,
  biochip: biochip,
  pareto: pareto,
  text: text
});

export default mainReducer
