<script>
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Dialog from '$lib/components/ui/dialog/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';

	// let { dialogOpen = true } = $props();
	let dialogOpen = false;
	let bucketName = '';

	const handleOnSubmit = () => {
		// todo: call api to check if bucket existed
		if (bucketName) {
			dialogOpen = false;
		}
	};
</script>

<Dialog.Root bind:open={dialogOpen}>
	<!-- <Dialog.Trigger class={buttonVariants({ variant: 'default' })}>Add Bucket</Dialog.Trigger> -->

	<Button onclick={() => (dialogOpen = true)}>Add Bucket</Button>

	<Dialog.Content class="sm:max-w-[450px]">
		<Dialog.Header>
			<Dialog.Title>Add Bucket</Dialog.Title>
			<Dialog.Description>Create your bucket with name</Dialog.Description>
		</Dialog.Header>
		<div class="grid gap-4 py-4">
			<div class="grid grid-cols-4 items-center gap-4">
				<Label for="bucekt-name" class="text-right">Bucket Name</Label>
				<Input id="bucekt-name" bind:value={bucketName} class="col-span-3" />
			</div>
		</div>
		<Dialog.Footer>
			<Button type="submit" onclick={handleOnSubmit}>Save changes</Button>
		</Dialog.Footer>
	</Dialog.Content>
</Dialog.Root>
