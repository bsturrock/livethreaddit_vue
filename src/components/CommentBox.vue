<template>
    <div class="chat">
        <Comment v-for='comment in shown_comments' :key='comment.id' @commentclick="handleCommentClick" :comment='comment' />
    </div>
    <form @submit.prevent='post' class='reply'>
        <textarea ref='replybox' v-bind:class="{replying: currently_replying}" spellcheck="false" v-model='usercomment'></textarea>
        <button v-if='!currently_replying' @click='postNonReply' class="reply-button"><i class="fas fa-share"></i></button>
        <button v-if='currently_replying'  class='reply-button replying'><i class="fas fa-reply-all"></i></button>
    </form>

</template>

<script>
import Comment from '../components/Comment.vue'
import { ref, computed, watchEffect } from 'vue'
import { onMounted, onUpdated, onUnmounted } from 'vue'
export default {
    components: {Comment},
    emits: ['lock'],
    props: ['logged_in', 'threadid'],
    setup(props, { emit }) {
        const counter = ref(0);
        const replying_to_user = ref('')
        const replying_to_id = ref('')
        const currently_replying = ref(false)
        const usercomment = ref('')
        const comment_queue = ref([])
        const shown_comments = ref([])
        const comments = ref([])
        const rate_max = 2000
        const rate_min = 50
        const leaving = ref(false)
        const replybox = ref(null)

        const rate = ref(computed(() => {
                let my_rate = 1000 * (5/comment_queue.value.length)
                if(my_rate >= rate_max){
                    my_rate = rate_max
                } else if (my_rate <= rate_min){
                    my_rate = rate_min
                }
                return my_rate
            }))

        watchEffect(() => {
            if(usercomment.value == '') {
                replying_to_user.value = ''
                replying_to_id.value = ''
                currently_replying.value = false
            }
        })

        const post = async () => {
            if (!currently_replying.value) {
                var data = {
                    threadid : props.threadid,
                    body : usercomment.value,
                    user_hash : props.logged_in,
                    reply : false
                }
                let response = await fetch('http://127.0.0.1:5000/post', {
                    method: 'POST',
                    headers: {'Content-Type' : 'application/json'},
                    body: JSON.stringify(data)
                })
                let response_json = await response.json()
                usercomment.value = ''
                }   
            else {
                let comment_body_info = usercomment.value.split(' ')
                comment_body_info = comment_body_info.slice(1)
                let comment_body = comment_body_info.join(' ')
                var data = {
                    threadid : props.threadid,
                    body : comment_body,
                    user_hash : props.logged_in,
                    reply : true,
                    replying_to : replying_to_id.value                   
                }
                let response = await fetch('http://127.0.0.1:5000/post', {
                    method: 'POST',
                    headers: {'Content-Type' : 'application/json'},
                    body: JSON.stringify(data)
                })
                let response_json = await response.json()
                usercomment.value = ''
            }
        }


        const returnNewComments = async () => {
            var data
            console.log(props.threadid,counter.value)
            let response = await fetch('http://127.0.0.1:5000/getcomments', {
                method: 'POST',
                headers: {'Content-Type' : 'application/json'},
                body: JSON.stringify({
                    threadid : props.threadid,
                    counter: counter.value,
                })
            })

            data = await response.json()
            if(data.status === 'locked'){
                emit('lock')
            }
            comments.value = data.comments
             

            if(data.status === 'success') {
                counter.value = data.counter + 1
                comment_queue.value = comments.value.concat(comment_queue.value)
                comments.value = []
            }
        }
        
        const moveCommentsToShown = () => {

            if(leaving.value) {
                console.log('clearing timeout')
                clearTimeout(moving_comments)
                moving_comments.value = null
                return
            }

            if(comment_queue.value.length === 0) {
                moving_comments.value = setTimeout(moveCommentsToShown, rate.value)
                return
            } else {
                const my_comment = comment_queue.value.pop()
                shown_comments.value.unshift(my_comment)
                removeComments()
                moving_comments.value = setTimeout(moveCommentsToShown, rate.value)
            }
        }
           
        const removeComments = () => {
            if (shown_comments.value.length > 100){
                shown_comments.value.pop()
            }
        }

        const handleCommentClick = (comment) => {

            usercomment.value = '@' + comment.author + ' '
            replying_to_user.value = comment.author
            replying_to_id.value = comment.id
            currently_replying.value = true
            replybox.value.focus()

        }

        const moving_comments = ref(setTimeout(moveCommentsToShown,200))
        const returning_comments = setInterval(returnNewComments, 3500);
        onUnmounted(() => {
            console.log('unmounting')
            clearInterval(returning_comments)
            leaving.value = true
        })
        
        return { comment_queue, shown_comments, usercomment, rate, counter, handleCommentClick, replybox, replying_to_user, currently_replying, replying_to_id, post}        
    }

}
</script>

<style>
* {
    margin: 0px;
    padding: 0px;
    box-sizing: border-box;
}

.chat {
    margin: auto;
    height: 75%;
    width: 99%;
    background: rgba(0,0,0,0.9);
    overflow-y: scroll;
    border: 1px solid  rgb(75,75,75);
}

.chat::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
    background-color: rgba(0,0,0,0.8);
}

.chat::-webkit-scrollbar {
    width: 6px;
    background-color: rgba(0,0,0,0.8);
    
}

.chat::-webkit-scrollbar-thumb {
    background-color: rgba(150,150,150);
}

.reply {
  display: flex;
  margin: auto;
  margin-top: 5px;
  width: 99%;
  align-items: stretch;
  height: 5%;
}

.reply textarea {
  padding: 5px;
  resize: none;
  height: 100%;
  display: block;
  flex: 9;
  border: none;
  background: rgba(0,0,0,1);
  color: white;
  border: 1px solid  rgb(75,75,75);
}

.reply textarea.replying {
    color: turquoise;
}

.reply textarea.replying:focus {
    outline: none;
    border: 1px solid turquoise;
    background: rgb(19, 36, 34);
}

.reply textarea:focus + .reply-button {
    border: 1px solid white;
    background: rgb(25,25,25);
}

.reply textarea.replying:focus + .reply-button.replying {
    border: 1px solid turquoise;
}

.reply-button.replying {
    color: turquoise;
    background: rgb(19, 36, 34);
}

.reply-button.replying:hover {
    background: rgb(29, 68, 64);
}

.reply textarea.replying {
        background: rgb(19, 36, 34);
}

.reply-button {
  height: 100%;
  display: block;
  flex: 1;
  background: rgba(0,0,0,1);
  color: white;
  border: none;
  margin-left: 5px;
  border: 1px solid rgb(75,75,75);
}

.reply-button:hover{
  background: rgba(50,50,50,1);
  cursor: pointer;
}

.reply textarea:focus {
  outline: none;
  border: 1px solid white;
  background: rgb(25,25,25);
}
</style>