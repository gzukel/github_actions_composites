## "SEND:DISCORD:MESSAGE"

This action will send a discord message to specific channel.

### Required Vars:
 - discord_token: "${{ secrets.DISCORD_TOKEN }}"
 - discord_channel_id: "${{ secrets.DISCORD_CHANNEL_ID }}"
 - discord_message: |
   discord message to send
   formatted.

```yaml
      - name: "SEND:DISCORD:MESSAGE"
        uses: gzukel/CosmosComposites/send_discord_message@main
        with:
          discord_token: "${{ secrets.DISCORD_TOKEN }}"
          discord_channel_id: "${{ secrets.DISCORD_CHANNEL_ID }}"
          discord_message: |
            GOVERNANCE PROPOSAL RAISE
            -------------------------
            VERSION: ${{ env.VERSION }}
            PROPOSAL_ID: ${{ env.GOV_PROPOSAL_NUM }}
            ESTIMATED_UPGRADE_DATETIME: ${{ env.UPGRADE_DATE }} UTC
            UPGRADE_HEIGHT: ${{ env.UPGRADE_HEIGHT }}
            
            UPGRADE_DESCRIPTION: 
            -------------------------
            ${{ env.RELEASE_DESCRIPTION }}
            
            VALIDATOR NOTES:
            -------------------------
            Please be prepared to upgrade your binary at the estimated time.
            It is our recommendation you set the upgrade-height as the halt-height in your application config.

```
