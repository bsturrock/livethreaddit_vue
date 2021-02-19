<template>
  <div @click='handleCommentClick' :id='comment.id' v-bind:class="{clicked:is_clicked}" class="comment">
        <div class="timestamp noselect">{{ comment.timestamp }}</div>
        <div class="comment-content noselect">
            <span class="author">{{ comment.author }} {{comment.counter}}:</span>
            <span class="body">{{ comment.body }}</span>
        </div>

  </div>
</template>

<script>
import { ref, watchEffect } from 'vue'
export default {
    props: ['comment', 'clicked_comment'],
    emits: ['commentclick'],
    setup(props, { emit }) {

        const is_clicked = ref(false)

        watchEffect(() => {
            if(props.clicked_comment == props.comment.id) {
                is_clicked.value = true
            } else {
                is_clicked.value = false
            }
        });

        const handleCommentClick = () => {
            emit('commentclick', props.comment)
        }


        return {handleCommentClick, is_clicked}

    }

}
</script>

<style>
    .comment {
        display: flex;
        padding: 5px;
        font-size: 14px;
    }

    .comment.clicked {
        background: rgb(58, 78, 76);
    }

    .comment.clicked .timestamp {
        color: white;
    }

    .comment.clicked:hover {
        background: rgb(82, 112, 109);
    }
    

    .comment div {
        font-family: 'Nunito';
        color: white;
        
    }

    .comment .author {
        font-weight: 1000;
        /* border-radius: 5px;
        background: rgb(124, 39, 39);
        color: white; */
        /* padding: 2px 2px 2px 2px; */
    }

    .author {
        padding-right: 10px;
    }

    .comment-content {
        flex: 1;
        text-align: left;
        padding-left: 10px;
    }

    .comment div.timestamp {
        color: rgb(120,120,120);
        font-family: 'Share Tech Mono';
        font-size: 10px;
        padding-top:5px;
    }

    .comment:hover {
        background: rgba(240, 240, 240,0.2);
        cursor: pointer;
    }

</style>