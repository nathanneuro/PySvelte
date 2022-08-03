<script>
    import { sparse_color_map_css } from "./shared_utils/colors";
    import { default as MapArrayImage } from "./components/MapArrayImage.svelte";
    import {default as ops} from "ndarray-ops";
    import LockableValueToggle from "./components/LockableValueToggle.svelte";


    // Pass in values for these
    // for editing puposes, make dummy vars for attention and pos/neg logits

    export let tokens;
    // export let attention; // the original/input. the one to use/display should be attention_show (below)
    export let model_map;
    export let layer_labels;
    // export let pos_logits;
    // export let neg_logits;
    // export let head_labels;
    export let show_tokens = true;
    export let current_tokens;
    export let num_clusters = 5;
    export let focus_token_map_index = 8;
    // export let blank_color = "#FFF";

    $: layer_labels = model_map[0]['layer_labels'];
    $: current_tokens = [model_map[focus_token_map_index - 1], model_map[focus_token_map_index]]

    export let focus_token_lock = { value: undefined, mode: "soft" };
    $: focus_token = focus_token_lock.value;
    // $: focus_token_map_index = the appropriate index somehow of the focused token...

    export let focus_head_lock = { value: undefined, mode: "soft" };
    $: focus_head = focus_head_lock.value;

    export let hover_token_is_target = false;

    // For a display element that isn't slow, can abstract over the switching between the original vs. info-weighted
    // by just using attention_show and letting svelte handle it.
    // However, as a heads-up for later in this fle, it can be too slow to re-draw / re-compute some aspects.
    // In the case of the ArrayImage components, we create both up front, and then display only the active one.
    // $: attention_show = attention
    // $: window.attention_show = attention_show;

    // export let _show_logits = false;
    // export let _show_neg_logits = false;

    function range(n) {
        return [...Array(n).keys()];
    }

    function reduce_Y(arr) {
        // reduces a 3d array to a 2d array by taking max of y, the column max
        if (arr === undefined) {
            return undefined;
        }
        var arr_ = [];
        for (var x = 0; x < arr.shape[0]; x++) {
            arr_.push([]);
            for (var c = 0; c < arr.shape[2]; c++) {
                var temp = 0;
                for (var y = 0; y < arr.shape[1]; y++) {
                    temp = Math.max(temp, arr.pick(x, y, c));
                }
                arr_[x].push(temp);
            }
        }
        return arr_;
    }

    function reduce_X(arr) {
        // reduces a 3d array to a 2d array by taking max of x, the row max
        if (arr === undefined) {
            return undefined;
        }
        var arr_ = [];
        for (var y = 0; y < arr.shape[0]; y++) {
            arr_.push([]);
            for (var c = 0; c < arr.shape[2]; c++) {
                var temp = 0;
                for (var x = 0; x < arr.shape[1]; x++) {
                    temp = Math.max(temp, arr.pick(x, y, c));
                }
                arr_[y].push(temp);
            }
        }
        return arr_;
    }

    // Cache both versions, to do less computation on them when switching
    // $: attention_reduce_dst = reduce_Y(attention);
    // $: attention_reduce_src = reduce_X(attention);

    // $: pos_logits_reduce_dst = reduce_Y(pos_logits);
    // $: pos_logits_reduce_src = reduce_X(pos_logits);

    // $: neg_logits_reduce_dst = reduce_Y(neg_logits);
    // $: neg_logits_reduce_src = reduce_X(neg_logits);

    // $: N_heads = attention.shape[2];
    // $: colors = range(N_heads).map((i) =>
    //     sparse_color_map_css(
    //         range(N_heads).map((x) => 1),
    //         undefined,
    //         i
    //     )
    // );
    // $: head_labels_ = head_labels != undefined ? head_labels : range(N_heads);

    function get_color(array, x, y, isolate_channel = undefined) {
        var v = array.pick(x, y, null);
        return sparse_color_map_css(v, undefined, isolate_channel);
    }

    function head_intensity(
        head_i,
        focus_token_value,
        hover_token_is_target,
        src_values,
        dst_values
    ) {
        if (focus_token_value == undefined) {
            var v = 1.0;
        } else {
            var reduced_array = hover_token_is_target ? src_values : dst_values;
            var v = Math.max(
                0,
                Math.min(1, reduced_array[focus_token_value][head_i])
            );
        }
        return "" + v;
    };

    function token_color(
        array,
        focus_token_value,
        tok_i,
        isolate_channel = undefined,
        hover_token_is_target,
        src_values,
        dst_values
    ) {
        if (focus_token_value == undefined) {
            var reduced_array = hover_token_is_target ? src_values : dst_values;
            return sparse_color_map_css(
                reduced_array[tok_i],
                undefined,
                isolate_channel
            );
            //return blank_color;
        }

        let tok_from = undefined;
        let tok_to = undefined;
        if (hover_token_is_target) {
            tok_from = tok_i;
            tok_to = focus_token_value;
        } else {
            tok_from = focus_token_value;
            tok_to = tok_i;
        }
        return get_color(array, tok_from, tok_to, isolate_channel);
    }

    function select_clusters(num_clusters, focus_token, current_tokens) {
        // should just be the selected focus token, but I'll get there eventually
        // with a filter on the model_map that says the name matches focus_token to select current_token 
        let current_token = current_tokens[1];
        let clusters = current_token["clusters"]
        console.log('clusters', clusters);
        clusters.sort(function (a,b) { 
            return a[3] - b[3];
        });
        // for (cluster in clusters) {
        //     let score = (0.0 * parseInt(cluster[0])) / parseInt(cluster[1]);
        //     console.log('cluster', cluster, score);

        // }
        return clusters.slice(0, num_clusters);
    }
    export let selected_clusters = [];
    $: selected_clusters = select_clusters(num_clusters, focus_token, current_tokens);

    // function select_current_tokens(
    //     tokens,
    //     focus_token_value,
    //     hover_token_is_target) {
    //         if (focus_token_value == undefined) {
    //             if (hover_token_is_target) {
    //                 return [tok_i];
    //             }
    //             return tokens;
    //         } else {
    //             return [focus_token_value];
    //         }
        
    //     }


    // export let all_attn_token_colors;
    // export let all_pos_logits_token_colors;
    // export let all_neg_logits_token_colors;

    // $: all_attn_token_colors = range(tokens.length).map(
    //     i => token_color(
    //                     attention_show,
    //                     focus_token,
    //                     i,
    //                     focus_head,
    //                     hover_token_is_target,
    //                     attention_reduce_src,
    //                     attention_reduce_dst
    //                 ));


    // export let all_token_colors;

    // $: all_token_colors = range(tokens.length).map(
    //     i => token_color(
    //                     attention_show,
    //                     focus_token,
    //                     i,
    //                     focus_head,
    //                     hover_token_is_target
    //                 ));
    // $: all_pos_logits_token_colors = range(tokens.length).map(
    //     i => token_color(
    //                     pos_logits,
    //                     focus_token,
    //                     i,
    //                     focus_head,
    //                     hover_token_is_target,
    //                     pos_logits_reduce_src,
    //                     pos_logits_reduce_dst
    //                 ));
    // $: all_neg_logits_token_colors = range(tokens.length).map(
    //     i => token_color(
    //                     neg_logits,
    //                     focus_token,
    //                     i,
    //                     focus_head,
    //                     hover_token_is_target,
    //                     neg_logits_reduce_src,
    //                     neg_logits_reduce_dst
    //                 ));



</script>
<div class="attn-container">
    
    <div class="figcaption" style="grid-column: big-attn;">
        <!-- here instead of showing a list of attention heads, I'm going to 
            show my full model layout:
            x axis tokens
            y axis: layers
             attention layer: attention heads
                - in the attention heads: clusters
            mlp layer
                - in mlp layer: clusters

            then off to the side of all this will be my top_matching_clusters list

            and somewhere, somehow, show the key/query/value divisions
            and the logit-lens

            The grand map of everything!!

            -->
        Importance Pattern for Selected Tokens
    </div>
    <div style="grid-column: big-attn; grid-row: main;">
        <table class="table">
            <thead>
                <tr>
                    <th>
                        layer_name
                    </th>
                {#each current_tokens as token_dict, token_dict_i}
                    
                        <th colspan="2">{token_dict['input_token']} </th>
                    
                {/each}
                </tr>
            </thead>
        
        <!-- html tables go row, column in definition I think -->
        <tbody>
            
        
        {#each layer_labels as layer, layer_i} 
        <tr>

            <td>{layer}</td>
            {#each current_tokens as token_dict, token_dict_i}
            
            <td>
                <MapArrayImage
                    array={token_dict['layer_viz'][layer_i]}
                    width="1600"
                    height="10"
                />
            </td>
            <td>
                {token_dict['logit_lens'][layer_i]}
            </td>

            {/each}

            </tr>
        {/each}

        <td>model output</td>
        {#each current_tokens as token_dict, token_dict_i}
            <td></td>
            <td>output_token:{token_dict['output_token']}</td>
        {/each}
        <tr>
        <td> Top Clusters for input token</td>
        </tr>
        <tr>
        <td></td>
        {#each current_tokens as token_dict, token_dict_i}
        <td>
            Clusters for {token_dict['input_token']}
        </td>
            {#each token_dict['sorted_clusters'] as cluster, cluster_i} 
                <tr>
                    <td>{cluster[0]}</td>
                    <td>{cluster[1]}</td>
                </tr>
            {/each}
        {/each}
    </tr>
    </tbody>
    </table>
    

    <div class="tokens-container">
            <div class="figcaption" style="grid-column: left;">
                Tokens (click to select)
            </div>
            <div class="tokens" style="grid-column: left;">
                {#each tokens as tok, tok_i}
                    <!-- n.b. it's important to not have any whitespace inside
                    the LockableValueToggle tag below, which is why we
                    format it like we do. See the comment inside
                    LockableValueToggle.html for more detail.
                  -->
                    <span
                    class="token {tok_i == focus_token ? 'selected' : ''}"
                    >{tok}</span>
                {/each}
            </div>

            <div style="grid-column: left;">
                Display options
                <div>
                    <select name="layer_viz" id="layer_viz">
                        <option value="default">Select a layer visualization</option>
                        <option value="neuron">Neuron-level importances</option>
                        <option value="layer">Layer-level importances</option>
                        <option value="weights">Weight matrix</option>
                      </select>
                      </div>
                <div>
                <div>
                    Visualization size:
                    <input type="range" id="layer_viz_width" name="layer_viz_width"
                            min="0" max="1600">
                    <label for="layer_viz_width">pixels</label>
                    <input type="range" id="layer_viz_height" name="layer_viz_height"
                            min="0" max="100">
                    <label for="layer_viz_height">pixels</label>
                    </div>
                <select name="factor_viz" id="factor_viz">
                    <option value="default">Select a factor visualization</option>
                    <option value="PCA">PCA</option>
                    <option value="NNMF">Non-negative Matrix factorization</option>
                    <option value="Model1">Custom Model 1</option>
                    <option value="Model2">Custom Model 2</option>
                  </select>
                  </div>
                  <div>
                   Top-n Clusters to show:
                    <input type="range" id="num_clusters" name="num_clusters"
                           min="0" max="5">
                    <label for="num_clusters">clusters</label>
                  </div>
                  <div>
                    Logit-lens top-n predicted tokens to show:
                    <input type="range" id="num_logit_tokens" name="num_logit_tokens"
                           min="0" max="5">
                    <label for="num_logit_tokens">tokens</label>
                  </div>

            </div>
    </div>
</div>
</div>

<style>
    table, th, td {
        border: 1px solid grey;
        border-collapse: collapse;
    }
    .attn-container {
        display: grid;
        grid-template-rows: [title] min-content [main] min-content;
        grid-template-columns: [big-attn] min-content [heads] minmax(
                min-content,
                624px
            );
        gap: 12px;
        
    }
    .figcaption {
        color: #888;
        grid-row: title;
        white-space: nowrap;
    }
    .tokens-container {
        display: grid;
        grid-template-rows: [title] min-content [main] min-content;
        grid-template-columns: [left] min-content [right] minmax(
                min-content,
                800px
            ) [end];
        gap: 12px;
        margin-top: 24px;
    }
    .tokens {
        grid-row: main;
        grid-column-start: left;
        grid-column-end: end;
        cursor: pointer;
        height: min-content;
        line-height: 110%;
    }
    .tokens .token {
        white-space: pre-wrap;
    }
    .tokens .selected {
        border: 1px solid #999;
        z-index: 10;
    }
    .tokens .token:not(.selected) {
        z-index: 0;
        padding: 1px;
    }
    .hover-mode,
    .hover-mode-text {
        color: #888;
        grid-row: title;
        grid-column: settings;
        cursor: pointer;
    }
    .hover-mode-text {
        margin-right: 8px;
    }


</style>
