const text = (state = "default 2", action) => {
    switch (action.type) {
        case 'UPDATE_TEXT':
            return state;
        default:
            return state;
    }
};

export default text; //to avoid no function errors
