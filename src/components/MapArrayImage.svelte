<script>
    import { onMount } from "svelte";
    // import {savePixels} from "save-pixels"

    export let array;
    export let width;
    export let height;
    export let width_multiplier = 0.3;
    export let height_multiplier = 2.0;
    // export let focus_token;
    let canvas;

    function draw(canvas, array, width, height) {
        if (canvas == undefined || array == undefined) {
            console.log('canvas or array is undefined')
            return;
        }
        console.log(array)
        canvas.width = width * width_multiplier;
        canvas.height = height;
        var ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.createImageData(1,1);
        // ctx.lineWidth = width_multiplier;
        for (var i = 0; i < array.length; i++) {
            var x = array[i][0];
            var y = array[i][1];
            var red = Math.floor(array[i][2]);
            var green = Math.floor(array[i][3]);
            var blue = Math.floor(array[i][4]);
            var alph = array[i][5];
            var w = array[i][6];
            var h = array[i][7];
            if (red + blue + green > 0) {
                ctx.fillStyle = 'rgba(' + red + ',' + blue + ',' + green + ',' + (alph / 255) + ')';
                ctx.fillRect(x * width_multiplier, y, w * width_multiplier, h * height_multiplier);
                // ctx.strokeStyle = 'white'
                if (i > 12) {
                    break;
                }
            }
            
        }
    }

    onMount(() => draw(canvas, array, width, height));
    $: draw(canvas, array, width, height);
</script>

<div class="container" style="width: {width * width_multiplier}px; height: {height * height_multiplier + 1}px">
    <canvas bind:this={canvas} style="width: {width * width_multiplier }px; height: {height * height_multiplier }px" />
</div>

<style>
    .container {
        position: relative;
        border: 1px solid rgb(255, 255, 255);
    }
    .container > * {
        position: absolute;
        width: 100%;
        left: 0px;
    }
    .container canvas {
        top: 0px;
        height: 100%;
        image-rendering: pixelated;
    }
    .container .focus-top,
    .container .focus-bottom {
        background: #aaa;
        opacity: 0.3;
    }
    .container .focus-top {
        top: 0px;
    }
    .container .focus-bottom {
        bottom: 0px;
    }
</style>
