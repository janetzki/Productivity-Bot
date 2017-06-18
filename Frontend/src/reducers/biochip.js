

const biochip = (state = {}, action) => {
    switch (action.type) {
        case 'INCREMENT':
            return state;
	case 'DECREMENT':
	    return state;
        default:
            return state;
    }
};

export default biochip; //to avoid no function errors.