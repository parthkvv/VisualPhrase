import React from 'react';

class AttentionOverlay extends React.Component {
    render() {
        let cols = this.props.array[0].length;

        return (
            <div className={`absolute bg-opacity-25 bg-black inset-0 grid grid-cols-${cols}`}>
                {this.props.array.map((row, i) => {
                    return (
                        row.map((alpha, j) => {
                            return (
                                <span key={i + j} className="attention-overlay-square w-full h-full" style={{ backgroundColor: `rgba(255, 255, 255, ${alpha})` }}></span>
                            );
                        })
                    )
                })}
            </div>
        )
    }
}

export default AttentionOverlay;